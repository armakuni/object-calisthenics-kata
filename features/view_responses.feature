Feature: View responses

    Scenario: View all responses for a questionnaire
        Given there is a questionnaire "Favourite Snacks" with questions
            | question  | type   |
            | question1 | text   |
            | question2 | yes/no |
        And there are cases for respondents
            | name    | email_address        |
            | Bob     | bob@minions.evil     |
            | Kevin   | kevin@minions.evil   |
            | Norbert | norbert@minions.evil |
        And "Bob" has submitted responses
            | question  | answer |
            | question1 | banana |
            | question2 | yes    |
        And "Kevin" has submitted responses
            | question  | answer      |
            | question1 | also banana |
            | question2 | no          |
        When I view the responses for the questionnaire "Favourite Snacks"
        Then I should see the responses
            | respondent | case_complete | question1   | question2 |
            | Bob        | yes           | banana      | yes       |
            | Kevin      | yes           | also banana | no        |
            | Norbert    | no            |             |           |

    Scenario: Trying to view responses for a questionnaire which doesn't exist gives an error
        Given there is no questionnaire with ID "16a62c71-2050-44ec-ab41-03d9b1cf531b"
        When I view the responses for the questionnaire with ID "16a62c71-2050-44ec-ab41-03d9b1cf531b"
        Then I receive an error "Questionnaire with ID 16a62c71-2050-44ec-ab41-03d9b1cf531b does not exist"
