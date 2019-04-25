<template>
  <div class="datatable-wrapper">
    <table class="datatable">
      <thead>
        <tr>
          <th
            v-for="col in cols"
            :key="col.field"
            :class="col.right ? 'text-right' : 'text-left'"
            :style="{ width: col.width }"
          >
            <button
              v-if="col.sortable"
              :title="`Sortieren nach ${col.label}`"
              @click="updateSort(col.field)"
              :class="col.sortBy ? 'text-green-500' : ''"
            >
              {{ col.label }}

              <svg class="inline fill-current h-3 w-3 ml-1" viewBox="0 0 20 20">
                <path
                  class="fill-current"
                  :class="col.sortBy === -1 ? 'text-green-500' : 'text-gray-300'"
                  d="M3.8 8.4h12.4c.3 0 .5-.1.7-.3l.2-.6c0-.3 0-.5-.2-.7L10.6.6a.9.9 0 0 0-.6-.2c-.2 0-.4 0-.6.2L3.2 6.8c-.2.2-.3.4-.3.7 0 .2 0 .4.3.6.1.2.4.3.6.3z"
                />
                <path
                  class="fill-current"
                  :class="col.sortBy === 1 ? 'text-green-500' : 'text-gray-300'"
                  d="M16.2 12H3.8c-.2 0-.5 0-.6.2l-.3.6c0 .2 0 .5.3.6l6.2 6.3.6.2c.3 0 .5 0 .6-.2l6.3-6.3.2-.6c0-.2 0-.4-.2-.6a.9.9 0 0 0-.7-.3z"
                />
              </svg>
            </button>
            <template v-else>
              {{ col.label }}
            </template>
          </th>
        </tr>
      </thead>

      <tbody>
        <tr v-if="data.length === 0" class="h-32">
          <td :colspan="cols.length" class="text-center text-bold">
            <slot name="empty">{{ emptyMessage }}</slot>
          </td>
        </tr>
        <tr
          v-for="row in paginatedRows"
          :key="row.pk"
          scope="row"
          :class="{ 'cursor-pointer': $listeners['rowClick'] }"
          @click="$emit('rowClick', row)"
        >
          <td
            v-for="col in cols"
            :key="col.field"
            :class="col.right ? 'text-right' : 'text-left'"
            :style="col.width ? `width: ${col.width}` : ''"
            style="font-variant-numeric: tabular-nums;"
          >
            <slot
              :name="col.field"
              v-bind="{
                value: row[col.field],
                formatter: col.formatter,
                row,
                col
              }"
            >
              {{ col.formatter(row[col.field], row) }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export interface Column {
  field: string;
  right: boolean;
  sortBy?: 1 | -1;
  label: string;
  sortable: boolean;
  formatter?: (value: any, row?: any) => string;
  sorter?: Sorter;
}

type Sorter = (a: object, b: object, sortField: string, sortDir: 1 | -1) => number;

const defaultSorter: Sorter = (a, b, sortField, sortDir) => {
  const x = a[sortField as keyof object] as any;
  const y = b[sortField as keyof object] as any;

  if (typeof x === 'string') {
    return x.localeCompare(y) * sortDir;
  }
  return (x - y) * sortDir;
};

export default Vue.extend({
  props: {
    data: { type: Array as () => object[], required: true },
    columns: { type: Array as () => Column[], required: true },
    defaultSortField: { type: String, default: '' },
    defaultSortDir: { type: Number as () => 1 | -1, default: 1 },
    perPage: { type: Number, default: 0 },
    currentPage: { type: Number, default: 1 },
    emptyMessage: { type: String, default: 'Keine Daten' }
  },
  data() {
    return {
      sortField: this.defaultSortField,
      sortDir: this.defaultSortDir
    };
  },
  computed: {
    cols(): Column[] {
      return (this.columns as Column[]).map((origCol) => {
        const col = { ...origCol };
        if (col.field === this.sortField) {
          col.sortBy = this.sortDir;
        } else {
          col.sortBy = undefined;
        }
        if (!col.formatter) {
          col.formatter = (v) => v;
        }
        return col;
      });
    },
    paginatedRows(): object[] {
      if (!this.perPage) {
        return this.sortedRows;
      }
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.sortedRows.slice(start, end);
    },
    sortedRows(): object[] {
      if (!this.sortField) {
        return this.data;
      }
      return this.data.slice().sort((a, b) => defaultSorter(a, b, this.sortField, this.sortDir));
    }
  },
  methods: {
    updateSort(field: string) {
      if (this.sortField === field) {
        this.sortDir = this.sortDir === 1 ? -1 : 1;
      } else {
        this.sortField = field;
        this.sortDir = 1;
      }
      this.$emit('sortChanged');
    }
  }
});
</script>


<style lang="postcss">
.datatable-wrapper {
  @apply shadow-md rounded-lg;
  width: 100%;
  overflow-x: auto;
}
@screen md {
  .datatable-wrapper {
    overflow-x: visible;
  }
}

.datatable {
  @apply bg-white rounded-lg text-sm;
  border-spacing: 0;
  border-collapse: separate;
  width: 100%;
}
@screen xl {
  .datatable {
    table-layout: fixed;
    @apply text-base;
  }
}

/* .datatable tr[scope='row']:nth-child(even) {
  background-color: rgba(0, 0, 0, 0.03);
} */
.datatable tr[scope='row']:hover {
  background-color: rgba(0, 0, 0, 0.03);
}

.datatable th {
  @apply relative bg-gray-150 px-2 font-bold sticky top-0 align-middle select-none;
  height: 3.5rem;
}
.datatable th button {
  @apply font-bold whitespace-no-wrap inline-flex items-center justify-start w-full h-full;
}
.datatable th button:focus {
  @apply outline-none;
}
.datatable th::after {
  @apply absolute inset-x-0	bottom-0 h-1 shadow-md;
  content: '';
}
.datatable th:first-child {
  @apply rounded-tl-lg;
  width: 30rem;
}
.datatable th:last-child {
  @apply rounded-tr-lg;
}

.datatable th:first-child,
.datatable td:first-child {
  @apply pl-6;
}
.datatable th:last-child,
.datatable td:last-child {
  @apply pr-6;
}

.datatable td {
  @apply px-2 align-middle border-b;
  height: 5rem;
}

.datatable td a {
  @apply inline-flex w-full items-center;
  height: 5rem;
}

.datatable td a:hover {
  @apply underline;
}
</style>
