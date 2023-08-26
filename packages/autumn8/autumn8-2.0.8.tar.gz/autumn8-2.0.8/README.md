# Autumn8 CLI

Autumn8 CLI is a toolkit, which allows you to easily interact programatically
with the Autumn8's ML service, AutoDL.

## Documentation

For the official, up-to-date documentation for the CLI,
go here:

[DOCUMENTATION](https://docs.google.com/document/d/1zcjHvVzeNRnS9-L3HRWBxUb1_i14IcvE/view)

## Example Usage

```
$ autumn8-cli --help
Usage: autumn8-cli [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  delete-model          Delete model from AutoDL
  deploy                Deploy a model from AutoDL onto cloud.
  get-model             Get model data from AutoDL
  list-deployments      List running deployments.
  login                 Store API credentials for the CLI for future use.
  run-docker            Run an inference on a given Docker image by...
  run-inference         Run an inference on a given deployment
  submit-checkpoint     Submit checkpoint to AutoDL
  submit-model          Submit a model to AutoDL.
  terminate-deployment  Terminate a running deployment.
  test-connection       Test AutoDL connection with the current API key.
```

### Logging In

To use the CLI - as a prerequisite, you'll have to log in into
autodl.autumn8.ai and generate an API key for you CLI from your Profile page.

Follow the instructions on https://autodl.autumn8.ai/profile
to authenticate your CLI.

```
$ autumn8-cli login --user_id $YOUR_USER_ID --api_key $YOUR_API_KEY
```

### Uploading Models

```
$ autumn8-cli submit-model --help
Usage: autumn8-cli submit-model [OPTIONS] MODEL_FILEPATH_OR_URL
                                [MODEL_SCRIPT_ARGS]...

  Submit a model to AutoDL.

Options:
  -n, --name TEXT                 Name of the model to be used in AutoDL.
  -t, --quantization, --quants [FP32|FP16|INT8]
                                  Quantization for the model.
  --input_dims TEXT               The model input dimensions, specified as a
                                  JSON array.
  -w, --max_upload_workers INTEGER
                                  The count of workers to use for multipart
                                  uploads; defaults to 4.
  --input_file TEXT               The model input filepath.
  -y, --yes                       Skip all confirmation input from the user.
  --skip_inputs                   Don't ask about inputs, let AutoDL try to
                                  infer them.
  -o, --organization_id, --org_id INTEGER
                                  The ID of the Organization to use
  -q, --quiet                     Skip additional logging, printing only
                                  necessary info
  -g, --group_id TEXT             The ID of the model group to add the model
                                  to.
  --help                          Show this message and exit.
```

Let's download an example input for our model:

```
$ wget -O ./whisper.json \
    https://autodl-public-assets.s3.amazonaws.com/sample-inputs/whisper.json
```

... and upload it to the Autumn8 AutoDL service - run:

```
$ autumn8-cli submit-model \
    --input_file ./whisper.json \
    https://autodl-public-assets.s3.amazonaws.com/sample-models/whisper.mar
```

then follow the on-screen instructions.

### Deploying Models

```
$ autumn8-cli deploy --help
Usage: autumn8-cli deploy [OPTIONS]

  Deploy a model from AutoDL onto cloud.

Options:
  -hw, -t, --machine_type TEXT    Server type to use for the deployment
  -o, --organization_id, --org_id INTEGER
                                  The ID of the Organization to use
  -q, --quiet                     Skip additional logging, printing only
                                  necessary info
  -m, --model_id INTEGER          Model ID to deploy
  -s, --schedule / -i, --immediate
                                  Schedule the deployment to run in the future
  --schedule_on TEXT              Schedule the deployment on given date
  --deployment_id TEXT            Update an existing deployment, retaining its
                                  URL
  -b, --deploy_best [latency|throughput|cost_performance|total_energy|emissions]
                                  Let Autumn8 pick the server type
                                  automatically for the deployment
  -c, --cloud_provider [a8f|gcp|aws|None|Amazon|Google Cloud Platform|Oracle|Azure|Autumn8]
                                  Cloud provider to use
  --help                          Show this message and exit.
```

We can roll out a model deployment with:

```
$ autumn8-cli deploy -c a8f -m $MODEL_ID -hw c5.large --org_id $YOUR_ORG_ID
```
