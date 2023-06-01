def blueprints():
    from .main import bp as main_bp
    from .users_controllers import bp as users_bp
    from .simulations_controllers import bp as simulations_bp

    return [main_bp, users_bp, simulations_bp]
