<template>
  <div v-if="hide_input">
      <h1 class="title" style="color:white;">Simple Text</h1>
    <br/>
    <br/>
    <br/>
      <el-form ref="form" :model="form">
      <el-form-item>
        <el-input type="textarea" v-model="form.desc" placeholder="Copy-paste your own text(s)..."></el-input>
      </el-form-item>
          <el-form-item>
        <el-select v-model="form.value" placeholder="Select English level">
          <el-option value="1" label="A1 (Beginner)"></el-option>
          <el-option value="2" label="A2 (Elementary English)"></el-option>
          <el-option value="3" label="B1 (Intermediate English)"></el-option>
          <el-option value="4" label="B2 (Upper-Intermediate English)"></el-option>
          <el-option value="5" label="C1 (Advanced English)"></el-option>
          <el-option value="6" label="C2 (Proficiency English)"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit()">Find Words</el-button>
      </el-form-item>
      <el-form-item>
        <el-button @click="reset()">Reset Text</el-button>
      </el-form-item>
      </el-form>
  </div>
  <div v-else>
    <h1 class="title" style="color:white;">Simple Text</h1>
    <br/>
    <br/>
  <div v-html="legacyHTML"></div><br/><br/>
    <div>
  <el-card class="box-card">
  <div slot="header" class="clearfix" align="left">
    <span>Words that you may not know:</span>
  </div>
  <div v-for="(wm, index) in wordMeaning" :key="`wm-${index}`" class="text item">
    {{wm[0]}}&nbsp;{{wm[2]}}
  </div>
  </el-card>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
        form: {
            desc: '',
            value: '6',
        },
        hide_input: true,
        errors: [],
        legacyHTML:'<div></div>',
        activeNames: ['1'],
        wordMeaning: {},
        output:''
    }
  },
  methods: {
      handleChange(val) {
        console.log(val);
      },
      reset() {
        this.form.desc = ''
      },
      async onSubmit() {
          this.hide_input = false
          try {
              const response = await axios.post(`http://127.0.0.1:5000/findwords`, {
                  text: this.form.desc, level: this.form.value
              })
              this.output = this.form.desc.replace(/\n/g, '<br>')
              //console.log(response['data'])
              this.wordMeaning = response['data']['new_text']
              var j;
              for (j = 0; j < response['data']['old_words'].length; j++) {
                var original_word = response['data']['old_words'][j]
                console.log(original_word)
                var first_idx = this.output.indexOf(original_word)
                var len = original_word.length
                this.output = `${this.output.slice(0, first_idx)}<span class="vocab">${this.output.slice(first_idx, first_idx+len)}
</span>${this.output.slice(first_idx+len, -1)}`
              }
              this.legacyHTML =`<div> ${this.output} </div>`;
          } catch (e) {
              this.errors.push(e)
          }
      }
  }
}
</script>

<style>
.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}
textarea {
    width: 100%;
    height: 50%;
    min-height: 200px!important;
}
.vocab {
  color: darkblue;
  font-weight:bold;
}
.text {
  font-size: 14px;
  text-align: left;
}

.item {
  padding: 18px 0;
}

.box-card {
  width: 480px;
  margin: auto!important;
}
</style>
