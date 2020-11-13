from steps.given import Given


class TestPosts:
    def test_when_there_are_no_posts(self, client):
        #
        # Given there are no posts
        # When the posts page is requested
        # It returns a 200 response with the generic 'empty state'
        #
        response = client.get('/posts')
        assert response.status_code == 200
        assert b'Hmm, there\'s nothing here' in response.data

    def test_when_there_are_some_posts(self, client):
        #
        # Given there are 5 posts
        # When the posts page is requested
        # It returns a 200 response with the list of posts
        #
        project = Given.a_project_exist()
        Given.a_bunch_of_posts_exist(project, 5)
        response = client.get('/posts')
        assert response.status_code == 200
        assert b'post-row' in response.data

    def test_when_there_are_more_than_25_projects_on_the_leaderboard(self, client):
        #
        # Given there are more than 25 posts
        # When the posts page is requested
        # It renders the pagination
        #
        project = Given.a_project_exist()
        Given.a_bunch_of_posts_exist(project, 26)
        response = client.get('/posts')
        assert response.status_code == 200
        assert b'pagination' in response.data
