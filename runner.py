import configargparse as argparse
import kfp
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("job_name", type=str, help="Name for job")
    parser.add_argument("-e", "--experiment_name", type=str, required=False, help="Experiment name")
    parser.add_argument("-p", "--pipeline_id", type=str, required=True, env_var='KF_PIPELINE_ID', help="Pipeline ID")
    parser.add_argument("--split_name", type=str, required=False, help="Split pattern; experiment name from job name")
    args = parser.parse_args()

    job_name: str = args.job_name

    if args.experiment_name:
        exp_name = args.experiment_name
    elif args.split_name:
        splits = job_name.split(args.split_name)
        if len(splits) < 2:
            # todo;; can this check move into argparse?
            raise ValueError(f"invalid split of the job name [{job_name}] with [{args.split_str}]")
        exp_name = splits[0]
        job_name = splits[-1]
    else:
        raise ValueError('either experiement_name or split_name are required ')

    print(f"j: {job_name} e: {exp_name}")

    client = kfp.Client()

    try:
        e = client.get_experiment(experiment_name=exp_name)
    except ValueError:
        e = client.create_experiment(exp_name)

    r = client.run_pipeline(e.id, job_name, pipeline_id=args.pipeline_id)

    print(r)
