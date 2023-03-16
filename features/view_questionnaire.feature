Feature: View questionnaire
    Scenario: Viewing a questionnaire
        Given there is a questionnaire "Favourite Snacks" with questions
            | question                                          | type   |
            | What is your favourite biscuit?                   | text   |
            | What is your favourite cheese?                    | text   |
            | How many snacks do you consume in a day?          | count  |
            | Should we be given free snacks during work hours? | yes/no |
        When I view the questionnaire
        Then the title should be "Favourite Snacks"
        And the questions should be
            | question                                          | type   |
            | What is your favourite biscuit?                   | text   |
            | What is your favourite cheese?                    | text   |
            | How many snacks do you consume in a day?          | count  |
            | Should we be given free snacks during work hours? | yes/no |

    Scenario: Trying to view a questionnaire which doesn't exist gives an error
        Given there is no questionnaire with ID "16a62c71-2050-44ec-ab41-03d9b1cf531b"
        When I view questionnaire "16a62c71-2050-44ec-ab41-03d9b1cf531b"
        Then I receive an error "Questionnaire with ID 16a62c71-2050-44ec-ab41-03d9b1cf531b does not exist"
