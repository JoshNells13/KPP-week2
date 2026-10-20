from rally_wasit.stage import generate_stage, is_rock, MIN_ROUTE_STEPS, route_length

SEEDS = range(300)


def test_same_seed_same_stage():
    assert generate_stage(7) == generate_stage(7)


def test_different_seeds_differ():
    assert generate_stage(1) != generate_stage(2)


def test_stage_is_playable():
    for seed in SEEDS:
        stage = generate_stage(seed)
        assert len(stage.rocks) == stage.width * stage.height
        assert not is_rock(stage, *stage.start), f'seed {seed}'
        assert not is_rock(stage, *stage.finish), f'seed {seed}'
        assert stage.start[0] == 0 and stage.finish[0] == stage.width - 1
        steps = route_length(stage)
        assert steps is not None and steps >= MIN_ROUTE_STEPS, f'seed {seed}'


def test_rock_rate_is_reasonable():
    rocks = sum(sum(generate_stage(seed).rocks) for seed in SEEDS)
    rate = rocks / (100 * len(SEEDS))
    assert 0.15 < rate < 0.30
