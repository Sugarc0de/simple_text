<template>
  <div class="container">
    <div position="absolute">
    <h1 class="title" style="color:white;">Simple Text</h1>
    <br/>
    <el-form>
      <el-form-item align="left">
        <el-button type="primary" @click="reset()">Back</el-button>
      </el-form-item>
      <el-form-item align="left">
        <p>Click the highlighted text to view its definition</p>
        <p>点击重点词汇即可查看注释</p>
      </el-form-item>
      <el-form-item>
        <DisplayText
          :jsonResults="getJson"
          :output="getOutput"
        />
      </el-form-item>
      <br/>
        <el-card class="box-card" align="center">
          <div slot="header" class="clearfix">
            <span>Words that you may not know:</span>
          </div>
          <div v-for="(wm, index) in wordMeaning" :key="`wm-${index}`" class="text item">
            {{wm[0]}}&nbsp;{{wm[2]}}
          </div>
        </el-card>
    </el-form>
  </div>
  </div>
</template>

<script>
  import DisplayText from "~/components/DisplayText";

  export default {
    components: {DisplayText},
    name: "Result",
    data() {
      return {
        wordMeaning: {},
        jsonResults: {}
      }
    },
    computed: {
      getJson() {
        this.wordMeaning = this.$store.state.jsonResults['new_text']
        return this.$store.state.jsonResults
      },
      getOutput() {
        return this.$store.state.output
      }
    },
    methods: {
      reset() {
        this.$router.push('/')
      }
    }
  }
</script>

<style>
  .container {
    margin: 3%;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    position: relative;
  }

  body {
    background-image: url(../static/background.jpeg);
    background-position: center top;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
    background-margin: 0% 0%;
    background-color: white;
  }
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
    width: auto;
    height: 50%;
    min-height: 200px;
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
    padding: 5px 0px;
    margin: 1%;
  }

  .box-card {
    margin-bottom: 5%;
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
</style>
