<template>
  <div v-html="original" align="left" class="result"></div>
</template>

<script>
    export default {
        name: "DisplayText",
        props: {
          jsonResults: {
            type: Object
          },
          output: {
            type: String
          }
        },
        data: function() {
          return {
            newOutput: '',
            new_text: this.jsonResults.new_text,
            old_words: this.jsonResults.old_words,
            original: this.output
          }
        },
        methods: {
          init() {
            var j;
            for (j = 0; j < this.old_words.length; j++) {
              var original_word = this.old_words[j]
              var first_idx = this.original.indexOf(original_word)
              var len = original_word.length
              this.original = `${this.original.slice(0, first_idx)}<span class="vocab">${this.original.slice(first_idx, first_idx + len)}</span>${this.original.slice(first_idx + len,)}`
            }
          }
        },
        mounted() {
            console.log('alright mounted')
            this.init()
        }
    }
</script>

<style scoped>
.result {
    padding: 5px;
    left: 300px;
    border: 1px dashed purple;
    width: 800px;
  }
</style>
