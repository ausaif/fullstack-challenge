<template>
  <v-card class="px-4 ma-2">
    <v-card-title class="text-h5 text-success"
      >Favorite Properties</v-card-title
    >
    <v-table density="compact">
      <thead>
        <tr>
          <th class="text-left">Full Address</th>
          <th class="text-left">Class Description</th>
          <th class="text-left">Estimated Market Value</th>
          <th class="text-left">Building Use</th>
          <th class="text-left">Building SQ FT</th>
          <th class="text-left">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in properties" :key="item.property_id">
          <td>{{ item.full_address }}</td>
          <td>{{ item.class_description }}</td>
          <td>${{ item.estimated_market_value }}</td>
          <td>{{ item.building_use }}</td>
          <td>{{ item.building_sq_ft }} sqft</td>
          <td>
            <v-btn
              density="compact"
              prepend-icon="mdi-minus"
              variant="outlined"
              color="error"
              @click.prevent.stop="removeUserProperty(item.property_id)"
              >Remove</v-btn
            >
          </td>
        </tr>
      </tbody>
    </v-table>
    <hr />
    <div class="d-flex justify-end align-center my-2">
      <span> {{ showingItems }}</span>
      <v-sheet class="mx-4">
        <v-select
          density="compact"
          v-model="filters.limit"
          @update:model-value="get_properties()"
          variant="outlined"
          :items="[10, 20, 50]"
          hide-details
        ></v-select>
      </v-sheet>
      <v-btn v-show="showPrevious" @click="previous()" variant="text"
        >Previous</v-btn
      >
      <v-btn v-show="showNext" @click="next()" variant="text">Next</v-btn>
    </div>
  </v-card>
</template>

<script setup>
import { ref, reactive, onBeforeMount, computed } from "vue";
import { useAppStore } from "@/store/app";

const properties = ref([]);
const totalCount = ref(null);
const filters = reactive({
  skip: 0,
  limit: 10,
});

const store = useAppStore();

const showPrevious = computed(() => {
  if (filters.skip === 0) return false;
  else return true;
});

const showNext = computed(() => {
  if (filters.skip + filters.limit >= totalCount.value) return false;
  else return true;
});

const showingItems = computed(() => {
  let start = filters.skip + 1;
  let end = filters.skip + filters.limit;
  if (totalCount.value === 0) {
    start = 0;
    end = 0;
  }
  if (totalCount.value < end) {
    end = totalCount.value;
  }
  return `Showing Items ${start} - ${end} of ${totalCount.value}`;
});

onBeforeMount(async () => {
  get_properties();
});

const next = () => {
  filters.skip += filters.limit;
  get_properties();
};

const previous = () => {
  filters.skip -= filters.limit;
  get_properties();
};

const buildUrl = () => {
  const params = Object.keys(filters).map(
    (filter) => `${filter}=${filters[filter]}`
  );
  return `${import.meta.env.VITE_API_BASE_URL}/users/properties?${params.join(
    "&"
  )}`;
};

const get_properties = async () => {
  const resp = await fetch(buildUrl(), {
    method: "GET",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "x-token": store.xToken,
    },
  });
  if (resp.ok) {
    const content = await resp.json();
    properties.value = content.data;
    totalCount.value = content.total_count;
  }
};

const removeUserProperty = async (property_id) => {
  const resp = await fetch(
    `${import.meta.env.VITE_API_BASE_URL}/users/properties/${property_id}`,
    {
      method: "DELETE",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "x-token": store.xToken,
      },
    }
  );
  if (resp.ok) {
    const tempList = [];
    for (const item of properties.value) {
      if (item["property_id"] !== property_id) tempList.push(item);
    }
    properties.value = tempList;
    totalCount.value--;
  }
};
</script>
