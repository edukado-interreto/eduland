<script setup>
import RichContentImage from "@/components/RichContentImage.vue";
import RichContentSound from "@/components/RichContentSound.vue";
</script>

<script>
export default {
  name: "RichContent",
  props: ["text"],
  computed: {
    tokens() {
      return this.text
        .split(RegExp("{((?:img|video|sound):[^}]+)}"))
        .map((t, i) => {
          if (i % 2 == 0) {
            return {
              type: "text",
              content: t,
            };
          }
          const [type, content] = t.split(/:(.*)/);

          const ret = {
            type,
            content,
          };

          if (type == "img") {
            const src = `/assets/media/uploads/${content}`;
            if (src) {
              ret.src = src;
            } else {
              ret.invalid_src = true;
            }
          }

          if (type == "video") {
            const id = this.get_youtube_id(content);
            if (id) {
              ret.embed_url = `https://www.youtube.com/embed/${id}`;
            } else {
              ret.invalid_url = true;
            }
          }

          if (type == "sound") {
            const src = `/assets/media/uploads/${content}`;
            if (src) {
              ret.src = src;
              //ret.mimetype="audio/mpeg"
            } else {
              ret.invalid_src = true;
            }
          }

          return ret;
        })
        .filter((t) => t.content);
    },
  },
  methods: {
    get_youtube_id(url) {
      let id = new URLSearchParams(url.replace(/^[^?]*/, "")).get("v");
      if (id) return id;

      id = url.match(/https?:\/\/youtu\.be\/(.*)/)?.[1];
      if (id) return id;

      return null;
    },
  },
};
</script>

<template>
  <template v-for="(t, i) in tokens">
    <span v-if="t.type == 'text'">{{ t.content }}</span>

    <template v-if="t.type == 'img'">
      <div v-if="t.invalid_src" class="text-grey">
        <v-icon small>mdi-alert-outline</v-icon>
        <i>Invalid image: {{ t.content }}</i>
      </div>
      <RichContentImage v-else :src="t.src" :content="t.content" />
    </template>

    <template v-if="t.type == 'video'">
      <div v-if="t.invalid_url" class="text-grey">
        <v-icon small>mdi-alert-outline</v-icon>
        <i>Invalid video url: {{ t.content }}</i>
      </div>
      <iframe
        v-else
        style="max-height: 150px; max-width: 100%"
        :src="t.embed_url"
        title="YouTube video player"
        frameborder="0"
        allow="
          accelerometer;
          autoplay;
          clipboard-write;
          encrypted-media;
          gyroscope;
          picture-in-picture;
        "
        allowfullscreen
      />
    </template>

    <template v-if="t.type == 'sound'">
      <div v-if="t.invalid_src" class="text-grey">
        <v-icon small>mdi-alert-outline</v-icon>
        <i>Invalid audio: {{ t.content }}</i>
      </div>
      <RichContentSound v-else :src="t.src" :content="t.content" />
    </template>
  </template>
</template>
