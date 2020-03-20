<template>
  <div align="left" class="result">
    <component :is="string && {template:string}"/>
  </div>
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
    data: function () {
      return {
        newOutput: '',
        new_text: this.jsonResults.new_text,
        old_words: this.jsonResults.old_words,
        original: this.output,
        originText: this.output.split(" "),
        string: undefined
      }
    },
    methods: {
      init() {
        var j;
        for (j = 0; j < this.old_words.length; j++) {
          var original_word = this.old_words[j]
          var first_idx = this.original.indexOf(original_word)
          // Todo: check for key words that break my program 
          var len = original_word.length
          this.original = `${this.original.slice(0, first_idx)}
<el-popover placement="top-start" width="200" title="${this.new_text[j][0]}" content="${this.new_text[j][2]}" trigger="click">
<span slot="reference" class="vocab">${this.original.slice(first_idx, first_idx + len)}
</span>
</el-popover>${this.original.slice(first_idx + len,)}`
        };
        this.string = "<div>".concat(this.original, "</div>");
      }
    },
    created() {
      setTimeout(this.init, 1000)
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
