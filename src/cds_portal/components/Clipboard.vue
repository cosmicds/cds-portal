<template>
  <v-btn tile icon x-small @click="copyToClipBoard">
    <v-icon>mdi-content-copy</v-icon>
  </v-btn>
</template>

<script>
export default {
  methods: {
      copyToClipBoard(textToCopy) {
        navigator.clipboard.writeText(this.student_username);
      },
    }
}
</script>