import configargparse as argparse
import urllib.parse as url
import kfp

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("job_name", type=str, help="Name for job")
    parser.add_argument("-e", "--experiment_name", type=str, required=False, help="Experiment name")
    parser.add_argument("-p", "--pipeline_id", type=str, required=True, env_var='KF_PIPELINE_ID', help="Pipeline ID")
    parser.add_argument("--split_on", type=str, default='/', help="Split pattern; derive experiment from job_name")
    args = parser.parse_args()

    job_name: str = url.unquote(args.job_name)

    if args.experiment_name:
        exp_name = args.experiment_name
    elif args.split_on:
        splits = job_name.split(args.split_on)
        if len(splits) < 2:
            # todo;; can this check move into argparse?
            raise ValueError(f"invalid split of the job name [{job_name}] on [{args.split_on}]")
        exp_name = splits[0]
        job_name = splits[-1]
    else:
        raise ValueError('either experiment_name or split_on are required ')

    print(f"j: {job_name} e: {exp_name}")

    client = kfp.Client()

    try:
        exp_id = client.get_experiment(experiment_name=exp_name)
    except ValueError:
        exp_id = client.create_experiment(exp_name)

    r = client.run_pipeline(exp_id.id, job_name, pipeline_id=args.pipeline_id)

    print(r)
