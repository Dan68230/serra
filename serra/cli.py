# Entry point for serra command line tool
import sys
import click
from serra.run import run_job_from_job_dir, update_package, create_job_yaml, run_job_from_aws, translate_job#, visualize_dag
from serra.databricks import create_job
from serra.translate import Translator
from serra.utils import validate_worksapce

@click.group()
def main():
    validate_worksapce()

@main.command(name="start")
@click.argument("job_name")
def cli_start(job_name):
    """Create a yaml for job_name inside the data folder
    """
    create_job_yaml(job_name)

@main.command(name="run")
@click.argument("job_name")
def cli_run_job_from_job_dir(job_name):
    """Run a specific job locally
    """
    run_job_from_job_dir(job_name)

@main.command(name="translate")
@click.argument("sql_path")
@click.option("--run", is_flag=True, default=False, required=False)
def cli_translator(sql_path, run):
    """Run a specific job locally
    """
    translate_job(sql_path, run)

@main.command(name="create_job")
@click.argument("job_name")
@click.option( "--log-level", type=click.Choice(['DEBUG', "INFO", "WARNING"], case_sensitive=False))
def cli_create_job(job_name, log_level):
    """Create a databricks job
    """
    create_job(job_name)

@main.command(name="update_package")
def cli_update_package():
    """Uploads package to aws, and restarts databricks cluster
    """
    update_package()
    
@main.command(name="docs")
@click.argument("job_name")
def cli_docs(job_name):
    # visualize_dag(job_name)
    pass
    
# only for use by databricks cluster
# Did not use click because there were wierd traceback errors
def serra_databricks():
    assert len(sys.argv) == 2
    job_name = sys.argv[1]
    run_job_from_aws(job_name)
    
if __name__ == '__main__':
  main()