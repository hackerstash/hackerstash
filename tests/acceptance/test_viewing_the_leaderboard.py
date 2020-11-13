from steps.given import Given


class TestLeaderboard:
    def test_when_the_leaderboard_is_empty(self, client):
        #
        # Given there are no projects
        # When the leaderboard is requested
        # It returns a 200 response with the generic 'empty state'
        #
        response = client.get('/leaderboard')
        assert response.status_code == 200
        assert b'Hmm, there\'s nothing here' in response.data

    def test_when_there_are_projects_on_the_leaderboard(self, client):
        #
        # Given there are 5 projects that are on the leaderboard
        # When the leaderboard is requested
        # It returns a 200 response with the list of projects
        #
        Given.a_bunch_of_projects_exist_on_the_leaderboard(5)
        response = client.get('/leaderboard')
        assert response.status_code == 200
        assert b'leaderboard-row' in response.data

    def test_when_there_are_more_than_25_projects_on_the_leaderboard(self, client):
        #
        # Given there are more than 25 projects on the leaderboard
        # When the leaderboard is requested
        # It renders the pagination
        #
        Given.a_bunch_of_projects_exist_on_the_leaderboard(26)
        response = client.get('/leaderboard')
        assert response.status_code == 200
        assert b'pagination' in response.data
