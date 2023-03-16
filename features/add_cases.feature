Feature: Add cases
    Scenario: Adding cases emails unique access codes
        Given there is a questionnaire
        When I create cases for the questionnaire for respondents
            | name   | email_address       |
            | Bob    | bob@minions.evil    |
            | Kevin  | kevin@minions.evil  |
            | Stuart | stuart@minions.evil |
        Then each respondent should should receive an email with a unique access code
        And the cases should not be completed

    Scenario: Addition cases to a questionnaire that doesn't exist gives an error
        Given there is no questionnaire with ID "16a62c71-2050-44ec-ab41-03d9b1cf531b"
        When I create some cases for questionnaire "16a62c71-2050-44ec-ab41-03d9b1cf531b"
        Then I receive an error "Questionnaire with ID 16a62c71-2050-44ec-ab41-03d9b1cf531b does not exist"
