import configargparse as argparse
import kfp

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("job_name", type=str, help="Name for job")
    parser.add_argument("-e", "--experiment_name", type=str, default='testing', help="Experiment name")
    parser.add_argument("-p", "--pipeline_id", type=str, required=True, env_var='KF_PIPELINE_ID', help="Pipeline ID")
    args = parser.parse_args()

    client = kfp.Client()

    try:
        e = client.get_experiment(experiment_name=args.experiment_name)
    except ValueError:
        e = client.create_experiment(args.experiment_name)

    client.run_pipeline(e.id, args.job_name, pipeline_id=args.pipeline_id)
