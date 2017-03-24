import app
import config
import coverage
import os
import pipreqs
import unittest

from coverage       import coverage
from flask_migrate  import Migrate, MigrateCommand
from flask_script   import Manager

app.tgeni.config.from_object('config.Config')
migrate = Migrate(app.tgeni, app.db)
manager = Manager(app.tgeni)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """ Run unit tests.
    """
    test_suite = unittest.TestLoader().discover('.', pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(test_suite)

@manager.command
def cover():
    """ Run tests and generate coverage report.
    """
    cov = coverage(branch=True, include='app/*')
    cov.start()
    test_suite = unittest.TestLoader().discover('.', pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(test_suite)
    # Generate report...
    print('Coverage Report:')
    cov.report()
    directory = directory=os.path.join(config.BASEDIR, 'coverage')
    cov.html_report(directory=directory)
    cov.erase()


if __name__ == '__main__':
    manager.run()
