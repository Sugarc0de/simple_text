<template>
  <div v-if="hide_input">
 <textarea name="text" class="bigtextarea" spellcheck="false"
           v-model="input"></textarea>
    <el-button type="primary" @click="onSubmit">Find Words</el-button>
  </div>
  <div v-else>
  <div v-html="legacyHTML">
  </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      input: '',
      hide_input: true,
      errors: [],
      legacyHTML:'<div></div>'
    }
  },
  methods: {
      async onSubmit() {
          this.hide_input = false
          try {
              const response = await axios.post(`http://127.0.0.1:5000/findwords`, {
                  text: this.input, level: '6'
              })
              this.input = this.input.replace(/\n/g, '<br>')
              var i;
              for (i = 0; i < response['data']['response'].length; i++) {
                var word_freq = response['data']['response'][i]
                var word = word_freq[0]
                var first_idx = this.input.indexOf(word)
                var len = word.length
                this.input = `${this.input.slice(0, first_idx)}<mark>${this.input.slice(first_idx, first_idx+len)}
</mark>${this.input.slice(first_idx+len, -1)}`
              }
              this.legacyHTML =`<div> ${this.input} </div>`;
          } catch (e) {
              this.errors.push(e)
          }
      }
  }
}
</script>

<style>
.bigtextarea {
    width: 100%;
    height: 40%;
    min-height: 200px;
}
</style>

