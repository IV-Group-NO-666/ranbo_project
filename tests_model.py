import os
import warnings
import importlib
from ranbo.models import Post
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class DatabaseConfigurationTests(TestCase):

    def setUp(self):
        pass

    def does_gitignore_include_database(self, path):
        """
        Takes the path to a .gitignore file, and checks to see whether the db.sqlite3 database is present in that file.
        """
        f = open(path, 'r')

        for line in f:
            line = line.strip()

            if line.startswith('db.sqlite3'):
                return True

        f.close()
        return False

    def test_databases_variable_exists(self):
        """
        Does the DATABASES settings variable exist, and does it have a default configuration?
        """
        self.assertTrue(settings.DATABASES,
                        f"{FAILURE_HEADER}Your project's settings module does not have a DATABASES variable, which is required. {FAILURE_FOOTER}")
        self.assertTrue('default' in settings.DATABASES,
                        f"{FAILURE_HEADER}You do not have a 'default' database configuration in your project's DATABASES configuration variable. {FAILURE_FOOTER}")

    def test_gitignore_for_database(self):
        """
        If you are using a Git repository and have set up a .gitignore, checks to see whether the database is present in that file.
        """
        git_base_dir = os.popen('git rev-parse --show-toplevel').read().strip()

        if git_base_dir.startswith('fatal'):
            warnings.warn(
                "You don't appear to be using a Git repository for your codebase. Although not strictly required, it's *highly recommended*. Skipping this test.")
        else:
            gitignore_path = os.path.join(git_base_dir, '.gitignore')

            if os.path.exists(gitignore_path):
                self.assertTrue(self.does_gitignore_include_database(gitignore_path),
                                f"{FAILURE_HEADER}Your .gitignore file does not include 'db.sqlite3' -- you should exclude the database binary file from all commits to your Git repository.{FAILURE_FOOTER}")
            else:
                warnings.warn(
                    "You don't appear to have a .gitignore file in place in your repository. We ask that you consider this! ")


class ModelTests(TestCase):
    """
    Are the models set up correctly, and do all the required attributes (post exercises) exist?
    """

    def setUp(self):
        user_py = User.objects.get_or_create(username='nannan')

        Post.objects.get_or_create(user=user_py[0],
                                   view_times=156,
                                   like_times=49,
                                   content="Today, the Tokyo Olympic Diving women's 10m platform singles final, Tokyo Olympic Team has nine gold and silver sweep! Quan Hongchan gold, Chen Yuxi silver!")

    def test_post_model(self):
        """
        Runs some tests on the Post model.
        Do the correct attributes exist?
        """
        user_py = User.objects.get(username='nannan')
        post = Post.objects.get(view_times=156)
        self.assertEqual(post.like_times, 49,
                         f"{FAILURE_HEADER}Tests on the Post model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(post.view_times, 156,
                         f"{FAILURE_HEADER}Tests on the Post model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(post.content,
                         "Today, the Tokyo Olympic Diving women's 10m platform singles final, Tokyo Olympic Team has nine gold and silver sweep! Quan Hongchan gold, Chen Yuxi silver!",
                         f"{FAILURE_HEADER}Tests on the Page model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(post.user, user_py,
                         f"{FAILURE_HEADER}Tests on the Post model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")

    def test_str_method(self):
        """
        Tests to see if the correct __str__() method has been implemented for each model.
        """
        user_py = User.objects.get(username='nannan')
        post = Post.objects.get(
            content="Today, the Tokyo Olympic Diving women's 10m platform singles final, Tokyo Olympic Team has nine gold and silver sweep! Quan Hongchan gold, Chen Yuxi silver!")

        self.assertEqual(str(user_py), 'nannan',
                         f"{FAILURE_HEADER}The __str__() method in the User class has not been implemented .{FAILURE_FOOTER}")


class AdminInterfaceTests(TestCase):
    """
    A series of tests that examines the authentication functionality (for superuser creation and logging in), and admin interface changes.
    Have all the admin interface tweaks been applied, and have the two models been added to the admin app?
    """

    def setUp(self):
        """
        Create a superuser account for use in testing.
        Logs the superuser in, too!
        """
        User.objects.create_superuser('testAdmin', 'email@email.com', 'adminPassword123')
        self.client.login(username='testAdmin', password='adminPassword123')

        user = User.objects.get_or_create(username='TestUser')[0]
        Post.objects.get_or_create(view_times=156,
                                   like_times=49,
                                   content='dsfdsfsdf h hg i gui ug ig', user=user)

    def test_admin_interface_accessible(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200,
                         f"{FAILURE_HEADER}The admin interface is not accessible. Check that you didn't delete the 'admin/' URL pattern in your project's urls.py module.{FAILURE_FOOTER}")

    def test_models_present(self):
        """
        Checks whether the two models are present within the admin interface homepage -- and whether Ranbo is listed there at all.
        """
        response = self.client.get('/admin/')
        response_body = response.content.decode()

        # Is the Ranbo app present in the admin interface's homepage?
        self.assertTrue('Models in the Ranbo application' in response_body,
                        f"{FAILURE_HEADER}The Ranbo app wasn't listed on the admin interface's homepage. You haven't added the models to the admin interface.{FAILURE_FOOTER}")

        # Check each model is present.
        self.assertTrue('User' in response_body,
                        f"{FAILURE_HEADER}The User model was not found in the admin interface. If you did add the model to admin.py, did you add the correct plural spelling (User)?{FAILURE_FOOTER}")
        self.assertTrue('Post' in response_body,
                        f"{FAILURE_HEADER}The Post model was not found in the admin interface. If you did add the model to admin.py, did you add the correct plural spelling (Post)?{FAILURE_FOOTER}")

    def test_post_display_changes(self):
        """
        Checks to see whether the Post model has had the required changes applied for presentation in the admin interface.
        """
        response = self.client.get('/admin/ranbo/post/')
        response_body = response.content.decode()

        # Headers -- are they all present?
        self.assertTrue('<div class="text"><a href="?o=1">User</a></div>' in response_body,
                        f"{FAILURE_HEADER}The 'user' column could not be found in the admin interface for the Post model -- if it is present, is it in the correct order?{FAILURE_FOOTER}")
        self.assertTrue('<div class="text"><a href="?o=2">Content</a></div>' in response_body,
                        f"{FAILURE_HEADER}The 'content' column could not be found in the admin interface for the Post model -- if it is present, is it in the correct order?{FAILURE_FOOTER}")
        self.assertTrue('<div class="text"><a href="?o=3">View times</a></div>' in response_body,
                        f"{FAILURE_HEADER}The 'view_times'  column could not be found in the admin interface for the Post model -- if it is present, is it in the correct order?{FAILURE_FOOTER}")
        self.assertTrue('<div class="text"><a href="?o=4">Like times</a></div>' in response_body,
                        f"{FAILURE_HEADER}The 'like_times'  column could not be found in the admin interface for the Post model -- if it is present, is it in the correct order?{FAILURE_FOOTER}")


class PopulationScriptTests(TestCase):
    """
    Tests whether the population script puts the expected data into a test database.
    All values that are explicitly mentioned in the book are tested.
    Expects that the population script has the populate() function, as per the book!
    """

    def setUp(self):
        """
        Imports and runs the population script, calling the populate() method.
        """
        try:
            import population_script
        except ImportError:
            raise ImportError(
                f"{FAILURE_HEADER}The tests could not import the populate_script. Check it's in the right location (the first ranbo_project directory).{FAILURE_FOOTER}")

        if 'populate' not in dir(population_script):
            raise NameError(
                f"{FAILURE_HEADER}The populate() function does not exist in the populate_script module. This is required.{FAILURE_FOOTER}")

        # Call the population script -- any exceptions raised here do not have fancy error messages to help readers.
        population_script.populate()

    def test_user(self):
        """
        There should be three user from populate_script -- memeda,yingyingying,jijizha.
        """
        user = User.objects.filter()
        user_len = len(user)
        user_strs = map(str, user)

        self.assertEqual(user_len, 3,
                         f"{FAILURE_HEADER}Expecting 3 user to be created from the populate_script module; found {user_len}.{FAILURE_FOOTER}")
        self.assertTrue('memeda' in user_strs,
                        f"{FAILURE_HEADER}The user 'memeda' was expected but not created by populate_script.{FAILURE_FOOTER}")
        self.assertTrue('yingyingying' in user_strs,
                        f"{FAILURE_HEADER}The user 'yingyingying' was expected but not created by populate_script.{FAILURE_FOOTER}")
        self.assertTrue('jijizha' in user_strs,
                        f"{FAILURE_HEADER}The user 'jijizha' was expected but not created by populate_script.{FAILURE_FOOTER}")
