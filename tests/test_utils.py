import logging
import pytest
import tempfile
import os

from constants.settings import Settings

logger = logging.getLogger(__name__)


def test_generate_mocked(mock_msg_gen):
    logger.debug("test_generate_mocked start")
    result = mock_msg_gen.generate("Test item description")
    assert result == "Generated text"
    mock_msg_gen.llm.invoke.assert_called_once()

def test_generate_prompt(message_generator):
    logger.debug("test_generate_prompt start")
    with tempfile.NamedTemporaryFile(delete=False) as prompt_file, \
         tempfile.NamedTemporaryFile(delete=False) as profile_file:
        try:
            prompt_file.write(b"This is a prompt with <PROFILE_PLACEHOLDER> and <WOMEN_PLACEHOLDER>.")
            profile_file.write(b"User profile content.")
            prompt_file.close()
            profile_file.close()

            # Update settings to use the temporary files
            message_generator.prompt_file_path = prompt_file.name
            message_generator.profile_file_path = profile_file.name

            prompt = message_generator.generate_prompt("Item description")
            assert "User profile content" in prompt
            assert "Item description" in prompt
            assert "<PROFILE_PLACEHOLDER>" not in prompt
            assert "<WOMEN_PLACEHOLDER>" not in prompt
        finally:
            os.unlink(prompt_file.name)
            os.unlink(profile_file.name)

def test_generate(message_generator):
    logger.debug("test_generate start")
    with tempfile.NamedTemporaryFile(delete=False) as prompt_file, \
         tempfile.NamedTemporaryFile(delete=False) as profile_file:
        try:
            # Provide detailed instructions in the prompt
            prompt_file.write(b"Hello, My name is <PROFILE_PLACEHOLDER>. My friend name is <WOMEN_PLACEHOLDER>. what is my name and my friend name?")
            profile_file.write(b"John Doe")
            prompt_file.close()
            profile_file.close()
            
            # Update settings to use the temporary files
            message_generator.prompt_file_path = prompt_file.name
            message_generator.profile_file_path = profile_file.name

            result = message_generator.generate("Return the message")
            # Assert the LLM's expected response
            assert Settings().DEFAULT_MESSAGE in result
        
        finally:
            os.unlink(prompt_file.name)
            os.unlink(profile_file.name)
