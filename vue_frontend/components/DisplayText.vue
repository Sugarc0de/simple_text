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
        originText: this.output.split(" "),
        string: undefined
      }
    },
    methods: {
      init() {
        var j;
        for (j = 0; j < this.old_words.length; j++) {
          var original_word = this.old_words[j]
          for (let k = 0; k < this.originText.length; k++) {
            if (this.originText[k].indexOf("<el-popover") !== -1) {
              continue
            }
            var first_idx = this.originText[k].indexOf(original_word);
            var len = original_word.length;
            if (first_idx !== -1 &&
              !this.originText[k].charAt(first_idx + len).match(/[a-z]/i) &&
            !this.originText[k].charAt(first_idx-1).match(/[a-z]/i)) {
              this.originText[k] = `${this.originText[k].slice(0, first_idx)}
    <el-popover placement="top-start" width="200" title="${this.new_text[j][0]}" content="${this.new_text[j][2]}" trigger="click">
    <span slot="reference" class="vocab">${this.originText[k].slice(first_idx, first_idx + len)}
    </span>
    </el-popover>${this.originText[k].slice(first_idx + len,)}`;
              break;
            }
          }
        }
      this.originText = this.originText.join(" ");
      this.string = "<div>".concat(this.originText, "</div>");
    }
    },
    mounted() {
      this.init()
    }
  }
</script>

<style scoped>
  .result {
    padding: 5px;
    border: 1px dashed purple;
  }
</style>
