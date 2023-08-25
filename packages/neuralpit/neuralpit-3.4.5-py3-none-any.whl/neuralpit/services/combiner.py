class NeuralPitDocumentCombiner():

    def combine(self,docs):
        s3_docs = [doc for doc in docs if doc.metadata['source']['source']=='s3']
        return self.combine_s3_docs(s3_docs)
        
    def combine_s3_docs(self,docs):
        results = []
        keys = []
        for doc in docs:
            if doc.metadata['source']['key'] not in keys:
                keys.append(doc.metadata['source']['key'])        
        for key in keys:
            grouped_docs = [doc for doc in docs if doc.metadata['source']['key']==key]
            grouped_docs.sort(key = lambda x:x.metadata['page']-x.metadata['chunk'])
            docs_together = ".".join([doc.page_content for doc in grouped_docs])
            results.append(docs_together)
        return '\n'.join(results)
    
combiner = NeuralPitDocumentCombiner()