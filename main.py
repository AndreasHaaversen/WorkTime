from datetime import timedelta
import typer
import dateparser
from durations_nlp import Duration


def main(start_time: str = typer.Option(..., prompt="When did you start working today?"),
         end_time: str = typer.Option(...,
                                      prompt="When did you finish working today?"),
         lunch_duration: str = typer.Option(..., prompt="How long was your lunch?")):
    typer.echo("Welcome to WorkTime!")
    parsed_start = dateparser.parse(start_time)
    parsed_end = dateparser.parse(end_time)
    if parsed_start is None or parsed_end is None:
        typer.echo("Could not parse times, try again!")
        raise typer.Abort()
    if parsed_end < parsed_start:
        typer.echo("Endtime cannot be before start time!")
        raise typer.Abort()
    parsed_duration = Duration(lunch_duration)
    start_msg = typer.style(parsed_start.strftime(
        "%H:%M"), fg=typer.colors.WHITE, bold=True, bg=typer.colors.GREEN)
    end_msg = typer.style(parsed_end.strftime(
        "%H:%M"), fg=typer.colors.WHITE, bold=True, bg=typer.colors.GREEN)
    duration_msg = typer.style(pretty_time_delta(parsed_duration.to_seconds(
    )), fg=typer.colors.WHITE, bg=typer.colors.GREEN)

    work_time = parsed_end - parsed_start
    minus_lunch = work_time - timedelta(seconds=parsed_duration.to_seconds())

    work_duration_msg = typer.style(
        f"{minus_lunch.total_seconds()/(60*60):.1f} hrs", fg=typer.colors.WHITE, bg=typer.colors.GREEN)

    out_msg = f"You started working at {start_msg}, and finished at {end_msg}, and had a {duration_msg} long lunch.\nThat means you´ve worked for {work_duration_msg} today! 🥳🥳"
    typer.echo(out_msg)


def pretty_time_delta(seconds):
    sign_string = '-' if seconds < 0 else ''
    seconds = abs(int(seconds))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%s%dd %dh %dm' % (sign_string, days, hours, minutes)
    elif hours > 0:
        return '%s%dh %dm' % (sign_string, hours, minutes)
    elif minutes > 0:
        return '%s%dm' % (sign_string, minutes)
    else:
        return '%s%ds' % (sign_string, seconds)


if __name__ == "__main__":
    typer.run(main)
