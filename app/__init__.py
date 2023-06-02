from app.live_simulations.domains.domain_model import SimulationRepository


__repo = None
def get_repo() -> SimulationRepository:
    global __repo
    if __repo is None:
        from .webapp import task_runner
        __repo = task_runner.repository
    return __repo
    