<template>
  <div>
  <div v-if="is_hide">
  <h1 class="title" style="color:white;font-size:10vw;">VOCABASSIST</h1>
  <br/>
  <br/>
  <br/>
  <br/>
  <el-row>
      <el-col :span="12"><FileUpload />
    </el-col>
    <el-col :span="12"><el-button @click="click_import_text">自动猜词</el-button></el-col>
    </el-row>
    </div>
  <div v-else>
      <component :is="currentComponent"></component>
  </div>
  </div>
</template>

<script>
    import FileUpload from "./FileUpload"
    import HelloWorld from '~/components/HelloWorld.vue'
    export default {
        name: "EntryPage",
        components: {FileUpload, HelloWorld},
        data() {
          return {
            is_hide: true,
            currentComponent: HelloWorld
          }
        },
        methods: {
          click_import_text() {
            this.is_hide = false
        }
      }


    }
</script>

<style scoped>
.title {
    font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    display: block;
    font-weight: 400;
    font-size: 100px;
    color: white;
    letter-spacing: 1px;
  }

.el-button {
  font-size: 18px;
  border: 3px solid #cf404d;
  background-color: #cf404d;
  color: white;
}
</style>
