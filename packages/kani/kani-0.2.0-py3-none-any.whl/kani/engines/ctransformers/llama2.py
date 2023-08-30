from kani.ai_function import AIFunction
from kani.models import ChatMessage, ChatRole
from .. import llama2_prompt
from .base import CTransformersEngine


class LlamaCTransformersEngine(CTransformersEngine):
    """Implementation of LLaMA v2 using ctransformers.

    You may also use the 7b or 13b models that use the LLaMA prompt.
    These models are converted from the original models in
    pytorch format to GGML format and can be found on huggingface.
    You can also download these models locally and pass the local path as an argument to the class.

    The huggingface GGML repos generally have multiple models in them (of different quantization levels),
    so you can choose the model depending inference speed, memory, and quality tradeoffs depending on the quantization
    performed on the model.

    A specific GGML model can be used from huggingface by passing the model id and the model file
    (e.g. https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML#provided-files) to
    `LlamaCTransformersEngine` and the model will be automatically downloaded and placed locally.

    Model IDs:

    - ``TheBloke/Llama-2-7B-Chat-GGML``
    - ``TheBloke/Llama-2-13B-chat-GGML``

    .. code-block:: python

        engine = LlamaCTransformersEngine("TheBloke/Llama-2-7B-Chat-GGML", model_file="llama-2-7b-chat.ggmlv3.q5_K_M.bin")
        ai = Kani(engine)

    .. tip:: The ``LlamaCTransformersEngine`` is a drop-in replacement for the :class:`.LlamaEngine`.

    .. seealso:: https://github.com/marella/ctransformers/tree/main#method-llmgenerate for generation parameters
    """

    def __init__(
        self,
        model_id: str = "TheBloke/Llama-2-7B-Chat-GGML",
        model_file: str = "llama-2-7b-chat.ggmlv3.q5_K_M.bin",
        *args,
        **kwargs,
    ):
        """
        :param model_id: The ID of the model to load from HuggingFace.
        :param model_file: The file of the model to load from HuggingFace repo or locally.
        :param max_context_size: The context size of the model.
        :param model_load_kwargs: Additional arguments to pass to ``AutoModelForCausalLM.from_pretrained()``.
        :param hyperparams: Additional arguments to supply the model during generation.
        """

        kwargs.setdefault("max_context_size", 4096)  # LLaMA has 4096 token window
        super().__init__(model_id, model_file, *args, **kwargs)

    def build_prompt(self, messages: list[ChatMessage], functions: list[AIFunction] | None = None) -> list[int]:
        return llama2_prompt.build(messages, tokenize=self.model.tokenize, eos_token_id=self.model.eos_token_id)

    def message_len(self, message: ChatMessage) -> int:
        # https://github.com/facebookresearch/llama/blob/main/llama/generation.py#L212
        if message.role == ChatRole.USER:
            # <s> [INST] {} [/INST] -> 7
            return len(self.model.tokenize(message.content)) + 7
        elif message.role == ChatRole.ASSISTANT:
            # {} </s> -> 2
            return len(self.model.tokenize(f" {message.content} ")) + 2
        # <s> [INST] <<SYS>>\n{}\n<</SYS>>\n\n [/INST] -> 20
        return len(self.model.tokenize(message.content)) + 20
