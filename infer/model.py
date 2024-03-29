#!/usr/bin/env python3

from infer.utils import load_F0, load_vocoder, load_starganv2, speakers, preprocess
import torch

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Model(metaclass=Singleton):
    def __init__(self) -> None:
        super().__init__()
        # support Hua_Chunying and Shi_Zhuguo
        Model.starganv2_1 = load_starganv2('epoch_00248.pth')
        # support Zhao_Lijian
        Model.starganv2_2 = load_starganv2('epoch_00742.pth')
        # set the default as None
        Model.starganv2 = None
        Model.F0_model = load_F0()
        Model.vocoder = load_vocoder()
        Model.speakers = speakers

    def compute_style(self, speaker_dicts):
        reference_embeddings = {}
        for key, (path, speaker) in speaker_dicts.items():
            # @lw: only use mapping network
            # @lw: speaker = idx of the speaker name
            label = torch.LongTensor([key]).to('cuda')
            latent_dim = self.starganv2.mapping_network.shared[0].in_features
            # @lw: get the reference embedding from the mapping network
            ref = self.starganv2.mapping_network(
                torch.randn(1, latent_dim).to('cuda'), label)
            reference_embeddings[key] = (ref, label)

        return reference_embeddings


    def infer(self, audio, speaker):
        '''@lw
        :speaker: the speaker name
        '''

        # @lw: set reference, get the speaker index
        speaker_dicts = {speaker: ('', self.speakers[speaker])}

        # @lw: compute reference embeddings
        reference_embeddings = self.compute_style(speaker_dicts)

        # conversion
        source = preprocess(audio).to('cuda:0')
        converted_audio = None

        for key, (ref, _) in reference_embeddings.items():
            with torch.no_grad():
                f0_feat = self.F0_model.get_feature_GAN(source.unsqueeze(1))
                out = self.starganv2.generator(source.unsqueeze(1), ref, F0=f0_feat)

                c = out.transpose(-1, -2).squeeze().to('cuda')
                y_out = self.vocoder.inference(c)
                y_out = y_out.view(-1).cpu()

            converted_audio = y_out.numpy()

        return converted_audio
