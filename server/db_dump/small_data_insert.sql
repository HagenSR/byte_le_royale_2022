INSERT INTO
    team_type(team_type_name, eligible)
VALUES
    ('Undergrad', true),
    ('Graduate', false),
    ('Alumni', false),
    ('Other', false);

INSERT INTO
    university(uni_name)
VALUES
    ('NDSU'),
    ('MSUM'),
    ('UND'),
    ('Other');

SELECT
    results.grouprunid,
    dense_rank() OVER (
        ORDER BY
            total_wins DESC
    ) as place,
    results.team_name,
    results.uni_name,
    results.start_run,
    results.total_wins,
    results.launcher_version
FROM
    (
        SELECT
            (get_leaderboard(true, group_run.group_run_id)).* as leaderboard
        FROM
            group_run
    ) as results
WHERE
    results.team_name = (
        Select
            team_name
        FROM
            team
        WHERE
            team.team_id = teamid
    )
ORDER BY
    leaderboards.group_run_id DESC;