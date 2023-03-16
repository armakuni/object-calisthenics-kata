Feature: Create questionnaire
    Scenario: Successfully creating a questionnaire
        When I create questionnaire with title "Favourite Snacks" with questions
            | question                                          | type   |
            | What is your favourite biscuit?                   | text   |
            | What is your favourite cheese?                    | text   |
            | How many snacks do you consume in a day?          | count  |
            | Should we be given free snacks during work hours? | yes/no |
        Then I should receive a questionnaire ID

    Scenario: Creating a questionnaire with no questions gives an error
        When I create questionnaire with title "Favourite Snacks" with no questions
        Then I receive an error "Questionnaire must have at least one question"

    Scenario: Creating a questionnaire with invalid question types gives an error
        When I create questionnaire with title "Favourite Snacks" with questions
            | question                                          | type   |
            | What is your favourite snack?                     | invalid|
        Then I receive an error "Invalid question type 'invalid' for question 'What is your favourite snack?'"
