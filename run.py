from app import create_app

#app_launch = create_app(config_name='dev')
if __name__ == "__main__":
    create_app(config_name='dev').run()