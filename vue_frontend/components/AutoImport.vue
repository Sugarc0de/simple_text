<template>
  <div>
    <div class="block">
      <el-cascader
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
          value: 'fiction',
          label: 'Fiction',
          children: [{
            value: 'A',
            label: 'Beginner',
            children: [{
              value: 'The Lion, the Witch, and the Wardrobe',
              label: 'Excerpt from The Lion, the Witch, and the Wardrobe'
            }]
          },
            {
              value: 'B',
              label: 'Intermediate',
              children: [{
              value: 'Invitation to the Game',
              label: 'Excerpt from Invitation to the Game'
            }]
            },
            {
              value: 'C',
              label: 'Advanced',
              children: [{
              value: 'The Hitchhiker’s Guide to the Galaxy',
              label: 'Excerpt from The Hitchhiker’s Guide to the Galaxy'
            }]
            }]
        }]
      }
    },
    methods: {
      async handleChange(value) {
        try {
              const response = await axios.get(`/app/samples`, {
                params: {genre: value[0], level: value[1]}
              })
              this.$emit('getData', {'text': response['data']['text'], 'level': value[1]});
            } catch (e) {
              this.errors.push(e)
            }
        }
    }
  }
</script>

<style scoped>

</style>
