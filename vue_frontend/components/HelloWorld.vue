<template>
  <div v-if="hide_input">
    <h1 class="title" style="color:white;">Simple Text</h1>
    <br/>
    <br/>
    <br/>
    <el-form ref="form" :model="form" :rules="rules">
      <el-form-item>
        <p>Copy and paste your own English text and the program will highlight difficult vocabulary based on your English level </p>
        <p align="left">复制粘贴任意英文文章，即可一键生成所有生词</p>
      </el-form-item>
      <el-form-item>
        <el-input type="textarea" v-model="form.desc" placeholder="Copy-paste your own text(s)..."></el-input>
      </el-form-item>
      <el-form-item prop="value">
        <el-select v-model="form.value" placeholder="Select English level">
          <el-option value="A1" label="A1 (Beginner)"></el-option>
          <el-option value="A2" label="A2 (Elementary English)"></el-option>
          <el-option value="B1" label="B1 (Intermediate English)"></el-option>
          <el-option value="B2" label="B2 (Upper-Intermediate English)"></el-option>
          <el-option value="C1" label="C1 (Advanced English)"></el-option>
          <el-option value="C2" label="C2 (Proficiency English)"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit('form')">Find Words</el-button>
      </el-form-item>
      <el-form-item>
        <el-button class="btn-reset" @click="reset()">Reset Text</el-button>
      </el-form-item>
    </el-form>
  </div>
  <div v-else>
    <h1 class="title" style="color:white;">Simple Text</h1>
    <br/>
    <br/>
    <p align="left">Click the highlighted text to view its definition</p>
    <br/>
    <p align="left">点击重点词汇上即可查看注释</p>
    <br/>
    <div>
      <DisplayText
        :jsonResults="jsonResults"
        :output="output"
      />
    </div>
    <br/><br/>
    <div>
      <el-card class="box-card">
        <div slot="header" class="clearfix" align="left">
          <span>Words that you may not know:</span>
        </div>
        <div v-for="(wm, index) in wordMeaning" :key="`wm-${index}`" class="text item">
          {{wm[0]}}&nbsp;{{wm[2]}}
        </div>
      </el-card>
      <br/>
      <el-button type="primary" @click="reset()">New Text</el-button>
    </div>
    <br/>
    <br/>
  </div>
</template>

<script>
  import axios from 'axios';
  import DisplayText from "./DisplayText";

  export default {
    components: {DisplayText},
    data() {
      return {
        form: {
          desc: '',
          value: '',
        },
        rules: {
          value: [
            {required: true}
          ]
        },
        hide_input: true,
        errors: [],
        legacyHTML: '',
        activeNames: ['1'],
        wordMeaning: {},
        output: '',
        jsonResults: {}
      }
    },
    methods: {
      handleChange(val) {
      },
      reset() {
        if (!this.hide_input) {
          this.hide_input = true
        }
        this.form.desc = ''
      },
      onSubmit(formName) {
        console.log(formName);
        this.$refs[formName].validate(async (valid) => {
          if (valid) {
            try {
              const response = await axios.post(`http://127.0.0.1:5000/findwords`, {
                text: this.form.desc, level: this.form.value
              })
              this.output = this.form.desc.replace(/\n/g, '<br>');
              //console.log(response['data'])
              this.jsonResults = response['data']
              this.wordMeaning = this.jsonResults['new_text']
              this.hide_input = false
            } catch (e) {
              this.errors.push(e)
            }
          } else {
            return false
          }
        })
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
    min-height: 200px !important;
  }

  .vocab {
    color: darkblue;
    font-weight: bold;
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
    margin: auto !important;
  }

  .el-form-item__error {
    color: #F56C6C;
    font-size: 14px;
    line-height: 1;
    padding-top: 4px;
    position: absolute;
    top: 20%;
    left: 0;
  }

  .el-button--primary {
    color: #fff;
    background-color: #778899;
    border-color: #778899;
  }

  .el-button--primary:hover {
    background-color: #b0c4de;
    border-color: #b0c4de;
  }

  .el-button--primary:focus {
    background-color: #b0c4de;
    border-color: #b0c4de;
  }

  .btn-reset:hover {
    color: #fff;
    background-color: #b0c4de;
    border-color: #b0c4de;
  }

  .btn-reset:hover {
    color: #fff;
    background-color: #b0c4de;
    border-color: #b0c4de;
  }
</style>
