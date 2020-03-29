<template>
  <div>
    <div class="block">
      <el-cascader
        transfer="true"
        placeholder="Import Text (Optional)"
        v-model="value"
        :options="options"
        @change="handleChange"></el-cascader>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  export default {
    name: "AutoImport",
    data() {
      return {
        value: [],
        errors: [],
        options: [{
            value: 'A',
            label: 'Beginner',
          },
            {
              value: 'B',
              label: 'Intermediate',
            },
            {
              value: 'C',
              label: 'Advanced',
            }
      ]
      }
    },
    methods: {
      async handleChange(value) {
        try {
              const response = await axios.get(`/app/samples`, {
                params: {genre: 'fiction', level: value[0]}
              })
              this.$emit('getData', {'text': response['data']['text'], 'level': value[0]});
            } catch (e) {
              this.errors.push(e)
            }
        }
    }
  }
</script>

<style scoped>

</style>
