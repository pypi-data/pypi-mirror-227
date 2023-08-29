# counts flops in an encoder-decoder model


def get_flops(
    num_layers_enc,
    num_layers_dec,
    hidden_size,
    num_heads,
    vocab_size,
    seq_len_enc,
    seq_len_dec,
    kv_channels=None,
    ffn_hidden_size=None,
    batch_size=1,
    recompute_granularity=None,
    glu_activation=False,
    iteration_time_in_sec=None,
    world_size=None,
):
    """Counts flops in an encoder-decoder model
    Args:
        num_layers_enc: number of encoder layers
        num_layers_dec: number of decoder layers
        hidden_size: hidden size of the model
        num_heads: number of heads in the model
        kv_channels: hidden size of the key and value heads
        ffn_hidden_size: hidden size of the FFN
        vocab_size: size of the vocabulary
        seq_len_enc: sequence length of the encoder
        seq_len_dec: sequence length of the decoder
        batch_size: batch size
        recompute_granularity: Activation recomputation method. Either None, "full" or "selective". Check Megatron-LM docs for more info.
        glu_activation: Whether to use GLU activation in FFN. Check T5 v1.1 for more info.
    Returns:
        model_flops: flops in the model (should be independent of the hardware and model implementation)
        hardware_flops: flops in the hardware (actual flops performed on the hardware). Check 6.3 in https://arxiv.org/pdf/2205.05198.pdf
    """

    if kv_channels is None:
        assert hidden_size % num_heads == 0
        kv_channels = hidden_size // num_heads
    if ffn_hidden_size is None:
        ffn_hidden_size = 4 * hidden_size

    # In the following we mark the reduced dimension with parentheses
    # encoder
    # self attention
    ## qkv projection
    encoder_qkv_proj_flops_fwd = (
        2 * num_layers_enc * batch_size * seq_len_enc * (hidden_size) * 3 * num_heads * kv_channels
    )
    ## qk logits
    encoder_qk_logits_flops_fwd = (
        2 * num_layers_enc * batch_size * num_heads * seq_len_enc * (kv_channels) * seq_len_enc
    )
    ## v logits
    encoder_v_logits_flops_fwd = (
        2 * num_layers_enc * batch_size * num_heads * seq_len_enc * (seq_len_enc) * kv_channels
    )
    ## attn out
    encoder_attn_out_flops_fwd = (
        2 * num_layers_enc * batch_size * num_heads * seq_len_enc * (kv_channels) * hidden_size
    )
    # FF
    ## 1st layer
    encoder_ffn_1_flops_fwd = 2 * num_layers_enc * batch_size * seq_len_enc * (hidden_size) * ffn_hidden_size
    if glu_activation:
        # 3 matmuls instead of 2 in FFN
        # ref. https://arxiv.org/pdf/2002.05202.pdf
        # Used for example in T5 v1.1
        encoder_ffn_1_flops_fwd = 4 * num_layers_enc * batch_size * seq_len_enc * (hidden_size) * ffn_hidden_size
    ## 2nd layer
    encoder_ffn_2_flops_fwd = 2 * num_layers_enc * batch_size * seq_len_enc * (ffn_hidden_size) * hidden_size

    encoder_flops_fwd = (
        encoder_qkv_proj_flops_fwd
        + encoder_qk_logits_flops_fwd
        + encoder_v_logits_flops_fwd
        + encoder_attn_out_flops_fwd
        + encoder_ffn_1_flops_fwd
        + encoder_ffn_2_flops_fwd
    )

    # decoder
    # self attention
    ## qkv projection
    decoder_self_qkv_proj_flops_fwd = (
        2 * num_layers_dec * batch_size * seq_len_dec * (hidden_size) * 3 * num_heads * kv_channels
    )
    ## qk logits
    decoder_self_qk_logits_flops_fwd = (
        2 * num_layers_dec * batch_size * num_heads * seq_len_dec * (kv_channels) * seq_len_dec
    )
    ## v logits
    decoder_self_v_logits_flops_fwd = (
        2 * num_layers_dec * batch_size * num_heads * seq_len_dec * (seq_len_dec) * kv_channels
    )
    ## attn out
    decoder_self_attn_out_flops_fwd = (
        2 * num_layers_dec * batch_size * num_heads * seq_len_dec * (kv_channels) * hidden_size
    )
    ## cross attention
    ## q projection
    decoder_cross_q_proj_flops_fwd = (
        2 * num_layers_dec * batch_size * seq_len_dec * (hidden_size) * num_heads * kv_channels
    )
    ## kv projection
    decoder_cross_kv_proj_flops_fwd = (
        2 * num_layers_dec * batch_size * seq_len_enc * (hidden_size) * 2 * num_heads * kv_channels
    )
    ## qk logits
    decoder_cross_qk_logits_flops_fwd = (
        2 * num_layers_dec * batch_size * num_heads * seq_len_dec * (kv_channels) * seq_len_enc
    )
    ## v logits
    decoder_cross_v_logits_flops_fwd = (
        2 * num_layers_dec * batch_size * num_heads * seq_len_dec * (seq_len_enc) * kv_channels
    )
    ## attn out
    decoder_cross_attn_out_flops_fwd = (
        2 * num_layers_dec * batch_size * num_heads * seq_len_dec * (kv_channels) * hidden_size
    )
    # FF
    ## 1st layer
    decoder_ffn_1_flops_fwd = 2 * num_layers_dec * batch_size * seq_len_dec * (hidden_size) * ffn_hidden_size
    if glu_activation:
        decoder_ffn_1_flops_fwd = 4 * num_layers_dec * batch_size * seq_len_dec * (hidden_size) * ffn_hidden_size
    ## 2nd layer
    decoder_ffn_2_flops_fwd = 2 * num_layers_dec * batch_size * seq_len_dec * (ffn_hidden_size) * hidden_size

    decoder_flops_fwd = (
        decoder_self_qkv_proj_flops_fwd
        + decoder_self_qk_logits_flops_fwd
        + decoder_self_v_logits_flops_fwd
        + decoder_self_attn_out_flops_fwd
        + decoder_cross_q_proj_flops_fwd
        + decoder_cross_kv_proj_flops_fwd
        + decoder_cross_qk_logits_flops_fwd
        + decoder_cross_v_logits_flops_fwd
        + decoder_cross_attn_out_flops_fwd
        + decoder_ffn_1_flops_fwd
        + decoder_ffn_2_flops_fwd
    )

    # lm head
    lm_head_flops_fwd = 2 * batch_size * seq_len_dec * (hidden_size) * vocab_size

    # the bwd pass requires double the flops in case of matmuls to calculate the gradients with respect to
    # both input and weight tensors
    model_flops = 3 * (encoder_flops_fwd + decoder_flops_fwd + lm_head_flops_fwd)  # 1 for fwd + 2 for bwd

    if recompute_granularity is None:
        hardware_flops = model_flops
    elif recompute_granularity == "full":
        # Note: we don't recompute lm head activs
        hardware_flops = model_flops + encoder_flops_fwd + decoder_flops_fwd  # + activ recomputation
    elif recompute_granularity == "selective":
        # all terms with s^2 are flops that are recomputed
        # ref. appendix A: https://arxiv.org/pdf/2205.05198.pdf
        recomputed_encoder_flops = encoder_qk_logits_flops_fwd + encoder_v_logits_flops_fwd
        recomputed_decoder_flops = (
            decoder_self_qk_logits_flops_fwd
            + decoder_self_v_logits_flops_fwd
            + decoder_cross_qk_logits_flops_fwd
            + decoder_cross_v_logits_flops_fwd
        )
        hardware_flops = model_flops + recomputed_encoder_flops + recomputed_decoder_flops
    else:
        raise ValueError("recompute_granularity must be one of 'full' or 'selective'")

    if iteration_time_in_sec is not None:
        model_flops = model_flops / (iteration_time_in_sec * world_size * 1e12)
        hardware_flops = hardware_flops / (iteration_time_in_sec * world_size * 1e12)

    return model_flops, hardware_flops


def get_flops_per_sec(
    iteration_time_in_sec,
    world_size,
    num_layers_enc,
    num_layers_dec,
    hidden_size,
    num_heads,
    vocab_size,
    seq_len_enc,
    seq_len_dec,
    kv_channels=None,
    ffn_hidden_size=None,
    batch_size=1,
    recompute_granularity=None,
    glu_activation=False,
):
    """Get flops per second for a given model"""
    model_flops, hardware_flops = get_flops(
        num_layers_enc=num_layers_enc,
        num_layers_dec=num_layers_dec,
        hidden_size=hidden_size,
        num_heads=num_heads,
        vocab_size=vocab_size,
        seq_len_enc=seq_len_enc,
        seq_len_dec=seq_len_dec,
        kv_channels=kv_channels,
        ffn_hidden_size=ffn_hidden_size,
        batch_size=batch_size,
        recompute_granularity=recompute_granularity,
        glu_activation=glu_activation,
    )
    model_flops_per_s = model_flops / (iteration_time_in_sec * world_size * 1e12)
    hardware_flops_per_s = hardware_flops / (iteration_time_in_sec * world_size * 1e12)
    return model_flops_per_s, hardware_flops_per_s
