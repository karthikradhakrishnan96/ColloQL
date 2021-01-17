from sentence_transformers import SentenceTransformer



class ColumnEncoder():
    def __init__(self, batch_size = 32):
        print("Loading sentence transformer model")
        self.model = SentenceTransformer('bert-large-nli-mean-tokens')
        self.batch_size = batch_size
        print("Loaded model")

    def encode_sample(self, sample):
        dummy_sentence = "The values in this column are " + " , ".join(sample)
        encoding = self.model.encode([dummy_sentence])[0]
        return encoding

    def encode_batch(self, samples):
        samples = ["The values in this column are " + " , ".join(sample) for sample in samples]
        encodings = self.model.encode(samples, batch_size=self.batch_size, show_progress_bar=True)
        return encodings

class ColumnEncoderSampler():
    def __init__(self, batch_size = 32):
        print("Loading sentence transformer model")

        print("Loaded model")

    def encode_sample(self, sample):
        # dummy_sentence = "The values in this column are " + " , ".join(sample)
        # encoding = self.model.encode([dummy_sentence])[0]
        return sample

    def encode_batch(self, samples):
        # samples = ["The values in this column are " + " , ".join(sample) for sample in samples]
        # encodings = self.model.encode(samples, batch_size=self.batch_size, show_progress_bar=True)
        return samples



class DummyColumnEncoder():
    def __init__(self, **kwargs):
        pass

    def encode_sample(self, sample):
        return [1,2,3]

    def encode_batch(self, samples):
        return [[1,2,3] for _ in samples]