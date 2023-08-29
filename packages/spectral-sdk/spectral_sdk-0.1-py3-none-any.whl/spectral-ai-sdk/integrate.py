import asyncio
import cloudpickle
import datetime
import ezkl
import json
import os
import requests
import torch
import zipfile

model_dir = './model'
model_onnx_path = model_dir + '/model.onnx'
model_compiled_onnx_path = model_dir + '/compiled_model.onnx'
model_settings_path = model_dir + '/settings.json'
model_witness_path = model_dir + '/witness.json'
model_vk_path = model_dir + '/model_vk.vk'
model_pk_path = model_dir + '/model_pk.pk'
model_srs_path = model_dir + '/kzg.srs'
model_proof_path = model_dir + '/zkml_hashed_proof.pf'
model_cal_path = model_dir + '/cal_data.json'
# cmd line args
pickle_model_path = './model/cloudpickle-model.pkl'
model_input_path = './model/input.json'

ipfs_node = 'http://8.8.8.8'


def zip_files(files, zip_name='model.zip'):
    zip_file = zipfile.ZipFile(zip_name, 'w')
    with zip_file:
        for file in files:
            zip_file.write(file, os.path.basename(file))
    print("Zipping [33] DONE " + str(datetime.datetime.now()))


def upload_to_ipfs(zip_path='model.zip'):

    url = f"{ipfs_node}:5001/api/v0/add"
    files = {'file': open(zip_path, 'rb')}
    response = requests.post(url, files=files)
    print(response.text)
    print("Uploading to IPFS [34] DONE " + str(datetime.datetime.now()))
    print(json.loads(response.text))
    return json.loads(response.text)['Hash']


if __name__ == '__main__':

    with open(pickle_model_path, 'rb') as f:
        data = f.read()
    model = cloudpickle.loads(data)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    input = torch.randn((1, 27), requires_grad=True).to(device)

    torch.onnx.export(model, input, model_onnx_path,
                      input_names=['input'],
                      output_names=['output'],
                      dynamic_axes={'input': {0: 'batch_size'},
                                    'output': {0: 'batch_size'}})
    x = input.detach().cpu().numpy().reshape([-1]).tolist()
    # convert to dict
    data = dict(input_data=[x])
    json.dump(data, open(model_input_path, 'w'))

    run_args = ezkl.PyRunArgs()
    run_args.input_visibility = 'public'
    run_args.param_visibility = 'public'
    run_args.output_visibility = 'public'
    run_args.batch_size = 1

    try:
        res = ezkl.gen_settings(model_onnx_path, model_settings_path,
                                py_run_args=run_args)
        if res:
            print('Settings successfully generated')
    except Exception as e:
        print(f'An error occurred: {e}')

    cal_data = {'input_data': input.detach().cpu().numpy().tolist()}
    # save as json file
    with open(model_cal_path, "w") as f:
        json.dump(cal_data, f)
        f.flush()
    # calibrate the settings file

        async def f():
            res = await ezkl.calibrate_settings(model_cal_path, model_onnx_path, model_settings_path,
                                                'resources')
            if res:
                print('Settings successfully calibrated')
            else:
                print('Settings calibration failed')
        asyncio.run(f())

    print("Calibration DONE " + str(datetime.datetime.now()))
    # get the SRS string

    try:
        res = ezkl.compile_model(
            model_onnx_path, model_compiled_onnx_path, model_settings_path)
        if res:
            print('Model successfully compiled')
    except Exception as e:
        print(f'An error occurred: {e}')

    res = ezkl.get_srs(model_srs_path, model_settings_path)
    print("SRS fetched " + str(datetime.datetime.now()))
    try:
        res = ezkl.gen_witness(
            model_input_path, model_compiled_onnx_path, model_witness_path, model_settings_path)
        if res:
            print('Witness file successfully generated')
    except Exception as e:
        print(f'An error occurred: {e}')
    print("Witness generated " + str(datetime.datetime.now()))

# mock proof for sanity check
try:
    res = ezkl.mock(model_witness_path,
                    model_compiled_onnx_path, model_settings_path)
    if res:
        print('Mock proof run was successfull')
except Exception as e:
    print(f'An error occurred: {e}')
print("In [29] DONE " + str(datetime.datetime.now()))
# ezkl setup - to generate PK and VK
try:
    res = ezkl.setup(model_compiled_onnx_path, model_vk_path,
                     model_pk_path, model_srs_path, model_settings_path)
    if res:
        print('Setup was successful')
except Exception as e:
    print(f'An error occurred: {e}')
print("In [30] DONE " + str(datetime.datetime.now()))
# generate proof
try:
    res = ezkl.prove(model_witness_path, model_compiled_onnx_path, model_pk_path, model_proof_path, model_srs_path,
                     'poseidon',  # 'evm' if proof required to be deployed onchain, 'poseidon' otherwise
                     'single', model_settings_path)
    if res:
        print('Proof was successfully generated')
except Exception as e:
    print(f'An error occurred: {e}')
print("In [31] DONE " + str(datetime.datetime.now()))


try:
    res = ezkl.verify(model_proof_path, model_settings_path,
                      model_vk_path, model_srs_path)
    if res:
        print('Proof was successfully verified')
except Exception as e:
    print(f'An error occurred: {e}')
print("In [32] DONE " + str(datetime.datetime.now()))

zip_files([model_srs_path, model_vk_path, model_settings_path])
hash = upload_to_ipfs()
