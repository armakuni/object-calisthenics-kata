Feature: Submit responses

    Scenario: Submitting responses with and invalid user access code gives an error
        Given there is no case with the user access code "111-999"
        When I submit responses for case "111-999"
        Then I receive an error "Case with UAC 111-999 does not exist"

    Scenario: Submitting complete response
        Given there is a questionnaire "Favourite Snacks" with questions
            | question                                          | type   |
            | What is your favourite cheese?                    | text   |
            | Should we be given free snacks during work hours? | yes/no |
        And there is a case for respondent "Bob" for the questionnaire
        When "Bob" submits the following responses
            | question                                          | answer |
            | What is your favourite cheese?                    | Brie   |
            | Should we be given free snacks during work hours? | yes    |
        Then the case should be completed

    Scenario: Submitting a response containing an unknown question gives an error
        Given there is a questionnaire "Favourite Snacks" with questions
            | question                                          | type   |
            | What is your favourite cheese?                    | text   |
        And there is a case for respondent "Kevin" for the questionnaire
        When "Kevin" submits the following responses
            | question                                          | answer |
            | What is your favourite cheese?                    | Brie   |
            | Should we be given free snacks during work hours? | yes    |
        Then "Kevin" receives an error "'Should we be given free snacks during work hours?' is not a question in 'Favourite Snacks'"

    Scenario: Submitting a response with missing questions gives an error
        Given there is a questionnaire "Favourite Snacks" with questions
            | question                                          | type   |
            | What is your favourite cheese?                    | text   |
            | Should we be given free snacks during work hours? | yes/no |
        And there is a case for respondent "Kevin" for the questionnaire
        When "Kevin" submits the following responses
            | question                                          | answer |
            | What is your favourite cheese?                    | Brie   |
        Then "Kevin" receives an error "'Should we be given free snacks during work hours?' is a question in 'Favourite Snacks' but has no answer"
