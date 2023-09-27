<template>
  <v-card class="px-4 ma-2">
    <v-card-title class="text-h5 text-success">Properties</v-card-title>
    <v-sheet>
      <v-card elevation="0">
        <v-card-title class="text-h6">Filters</v-card-title>
        <v-row>
          <v-col>
            <v-text-field
              v-model="filters.full_address"
              density="compact"
              variant="outlined"
              label="Full Address"
              hide-details
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="filters.class_id"
              density="compact"
              variant="outlined"
              label="Class Id"
              hide-details
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="filters.min_estimated_market_value"
              density="compact"
              variant="outlined"
              label="Minimum Estimated Market Value"
              hide-details
            ></v-text-field> </v-col
          ><v-col>
            <v-text-field
              v-model="filters.max_estimated_market_value"
              density="compact"
              variant="outlined"
              label="Maximum Estimated Market Value"
              hide-details
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              v-model="filters.building_use"
              density="compact"
              variant="outlined"
              label="Building Use"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="filters.min_building_sq_ft"
              density="compact"
              variant="outlined"
              label="Minimum Building SQ FT"
            ></v-text-field> </v-col
          ><v-col>
            <v-text-field
              v-model="filters.max_building_sq_ft"
              density="compact"
              variant="outlined"
              label="Maximum Building SQ FT"
            ></v-text-field>
          </v-col>
          <v-col class="d-flex justify-space-around">
            <v-btn
              @click="applyFilters()"
              color="primary"
              :disabled="disableFilter"
              >Apply Filters</v-btn
            >
            <v-btn
              class="ml-2"
              @click="resetFilters()"
              :disabled="disableFilter"
              >Reset Filters</v-btn
            >
          </v-col>
        </v-row>
      </v-card>
    </v-sheet>
    <hr />
    <v-card elevation="0" :loading="tableLoading">
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
                prepend-icon="mdi-plus"
                variant="outlined"
                color="success"
                :disabled="item.disabled"
                @click.prevent.stop="addUserProperty(item.property_id)"
                >Add</v-btn
              >
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
    <hr />
    <div class="d-flex justify-end align-center my-2">
      <span> {{ showingItems }}</span>
      <v-sheet class="mx-4">
        <v-select
          density="compact"
          v-model="filters.limit"
          @update:model-value="getProperties()"
          variant="outlined"
          :items="[10, 20, 50]"
          hide-details
        ></v-select>
      </v-sheet>
      <v-btn v-show="showPrevious" @click="previous()" variant="text"
        prepend-icon="mdi-arrow-left" >Previous</v-btn
      >
      <v-btn v-show="showNext" @click="next()" variant="text" append-icon="mdi-arrow-right">Next</v-btn>
    </div>
  </v-card>
</template>

<script setup>
import { ref, reactive, onBeforeMount, computed } from "vue";
import { useAppStore } from "@/store/app";

const properties = ref([]);
const totalCount = ref(null);
const tableLoading = ref(false);
const filters = reactive({
  full_address: null,
  class_id: null,
  min_estimated_market_value: null,
  max_estimated_market_value: null,
  building_use: null,
  min_building_sq_ft: null,
  max_building_sq_ft: null,
  skip: 0,
  limit: 10,
});
const userPropertyIds = reactive(new Set());

const store = useAppStore();

const effectiveFilters = computed(() => {
  return Object.keys(filters).filter((key) => filters[key] !== null);
});

const disableFilter = computed(() => {
  return (
    effectiveFilters.value.filter(
      (filter) => filter !== "limit" && filter !== "skip"
    ).length === 0
  );
});

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
  getUserPropertyIds();
  getProperties();
});

const next = () => {
  filters.skip += filters.limit;
  getProperties();
};

const previous = () => {
  filters.skip -= filters.limit;
  getProperties();
};

const applyFilters = () => {
  filters.skip = 0;
  getProperties();
};

const resetFilters = () => {
  filters.full_address = null;
  filters.class_id = null;
  filters.min_estimated_market_value = null;
  filters.max_estimated_market_value = null;
  filters.building_use = null;
  filters.min_building_sq_ft = null;
  filters.max_building_sq_ft = null;
  filters.skip = 0;
  getProperties();
};

const buildUrl = () => {
  const params = effectiveFilters.value.map(
    (filter) => `${filter}=${filters[filter]}`
  );
  return `${import.meta.env.VITE_API_BASE_URL}/properties?${params.join("&")}`;
};

const getUserPropertyIds = async () => {
  const resp = await fetch(
    `${import.meta.env.VITE_API_BASE_URL}/users/properties/ids`,
    {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "x-token": store.xToken,
      },
    }
  );
  if (resp.ok) {
    const content = await resp.json();
    for (const item of content) {
      userPropertyIds.add(item);
    }
  }
};

const getProperties = async () => {
  tableLoading.value = true;
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
    for (const item of content.data) {
      if (userPropertyIds.has(item["property_id"])) item["disabled"] = true;
      else item["disabled"] = false;
    }
    properties.value = content.data;
    totalCount.value = content.total_count;
  }
  tableLoading.value = false;
};

const addUserProperty = async (property_id) => {
  const resp = await fetch(
    `${import.meta.env.VITE_API_BASE_URL}/users/properties`,
    {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "x-token": store.xToken,
      },
      body: JSON.stringify({
        property_id,
      }),
    }
  );
  if (resp.ok) {
    for (const item of properties.value) {
      if (item["property_id"] === property_id) item["disabled"] = true;
    }
  }
};
</script>
