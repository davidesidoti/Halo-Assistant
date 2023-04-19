import spacy
from spacy.matcher import Matcher

# Load the language model
nlp = spacy.load('en_core_web_sm')

# Define a function to extract relevant information from the user's command


def extract_information(text):
    # Initialize the Matcher
    matcher = Matcher(nlp.vocab)

    # Define patterns to match
    weather_pattern = [{'LOWER': 'weather'}]
    location_pattern = [{'ENT_TYPE': 'GPE'}]
    landmark_pattern = [{'LOWER': {'IN': ['where', 'what']}},
                        {'LEMMA': 'be'},
                        {'ENT_TYPE': 'FAC'}]
    remind_pattern = [{'LOWER': {'IN': ['remind', 'remember']}},
                      {}]

    # Add patterns to the Matcher
    matcher.add('WEATHER_PATTERN', [weather_pattern])
    matcher.add('LOCATION_PATTERN', [location_pattern])
    matcher.add('LANDMARK_PATTERN', [landmark_pattern])

    # Parse the input text using the nlp model
    doc = nlp(text)

    # Use the Matcher to find matches in the text
    matches = matcher(doc)

    # Extract relevant information from the matches
    for match_id, start, end in matches:
        if nlp.vocab.strings[match_id] == 'WEATHER_PATTERN':
            # User is asking about the weather
            for entity in doc.ents:
                if entity.label_ == 'GPE':
                    # User specified a location
                    return {'intent': 'weather', 'location': entity.text}
            # User did not specify a location
            return {'intent': 'weather'}
        elif nlp.vocab.strings[match_id] == 'LOCATION_PATTERN':
            # User is asking about a location
            return {'intent': 'location', 'location': doc[start:end].text}
        elif nlp.vocab.strings[match_id] == 'LANDMARK_PATTERN':
            # User is asking about the location of a landmark or attraction
            return {'intent': 'location', 'location': doc[end:].text}

    # User did not ask about weather or location
    return {'intent': 'unknown'}


while True:
    # Tokenize the user's text
    doc = nlp(input('Command: '))
    
    for token in doc:
        print(f'Token: {token.text} -- Token lemma: {token.lemma_} -- Token pos: {token.pos_} -- Token ent: {token.ent_type_}')

    # Extract relevant information from the user's command
    information = extract_information(doc)

    # Print the extracted information
    print(information)
