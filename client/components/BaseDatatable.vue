<template>
  <div class="datatable-wrapper">
    <table class="datatable">
      <thead>
        <tr>
          <th
            v-for="col in cols"
            :key="col.field"
            :class="col.right ? 'text-right' : 'text-left'"
            :style="{ maxWidth: col.width }"
            :title="col.tooltip"
          >
            <button
              v-if="col.sortable"
              class="hover:text-gray-800 focus:text-gray-800"
              @click="updateSort(col.field)"
            >
              {{ col.label }}

              <svg class="inline fill-current h-3 w-3 ml-1" viewBox="0 0 20 20">
                <path
                  class="fill-current"
                  :class="col.sortBy === -1 ? 'text-gray-700' : 'text-gray-400'"
                  d="M3.8 8.4h12.4c.3 0 .5-.1.7-.3l.2-.6c0-.3 0-.5-.2-.7L10.6.6a.9.9 0 0 0-.6-.2c-.2 0-.4 0-.6.2L3.2 6.8c-.2.2-.3.4-.3.7 0 .2 0 .4.3.6.1.2.4.3.6.3z"
                />
                <path
                  class="fill-current"
                  :class="col.sortBy === 1 ? 'text-gray-700' : 'text-gray-400'"
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
            <slot name="empty">
              {{ emptyMessage }}
            </slot>
          </td>
        </tr>
        <tr
          v-for="row in paginatedRows"
          :key="row.pk"
          scope="row"
          :class="{ 'cursor-pointer': $listeners['rowClick'] }"
          :tabindex="$listeners['rowClick'] ? 0 : null"
          @click="$emit('rowClick', row)"
          @keypress.enter="$emit('rowClick', row)"
        >
          <td
            v-for="col in cols"
            :key="col.field"
            :class="col.right ? 'text-right' : 'text-left'"
            :style="{ maxWidth: col.width }"
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

<script>
// export interface Column {
//   field: string;
//   right: boolean;
//   sortBy?: 1 | -1;
//   label: string;
//   tooltip?: string;
//   sortable: boolean;
//   formatter?: (value: any, row?: any) => string;
//   width?: string;
// }

// type Sorter = (a: object, b: object, sortField: string, sortDir: 1 | -1) => number;

const defaultSorter = (a, b, sortField, sortDir) => {
  const x = a[sortField]
  const y = b[sortField]

  if (typeof x === 'string') {
    return x.localeCompare(y) * sortDir
  }
  return (x - y) * sortDir
}

export default {
  props: {
    data: { type: Array, required: true },
    columns: { type: Array, required: true },
    defaultSortField: { type: String, default: '' },
    defaultSortDir: { type: Number, default: 1 },
    perPage: { type: Number, default: 0 },
    currentPage: { type: Number, default: 1 },
    emptyMessage: { type: String, default: 'Keine Daten' }
  },
  data() {
    return {
      sortField: this.defaultSortField,
      sortDir: this.defaultSortDir
    }
  },
  computed: {
    cols() {
      return this.columns.map(origCol => {
        const col = { ...origCol }
        if (col.field === this.sortField) {
          col.sortBy = this.sortDir
        } else {
          col.sortBy = undefined
        }
        if (!col.formatter) {
          col.formatter = v => v
        }
        return col
      })
    },
    paginatedRows() {
      if (!this.perPage) {
        return this.sortedRows
      }
      const start = (this.currentPage - 1) * this.perPage
      const end = start + this.perPage
      return this.sortedRows.slice(start, end)
    },
    sortedRows() {
      if (!this.sortField) {
        return this.data
      }
      return this.data
        .slice()
        .sort((a, b) => defaultSorter(a, b, this.sortField, this.sortDir))
    }
  },
  methods: {
    updateSort(field) {
      if (this.sortField === field) {
        this.sortDir = this.sortDir === 1 ? -1 : 1
      } else {
        this.sortField = field
        this.sortDir = 1
      }
      this.$emit('sortChanged')
    }
  }
}
</script>

<style lang="postcss">
.datatable-wrapper {
  @apply shadow rounded;
  width: 100%;
}

.datatable {
  @apply bg-white rounded text-sm;
  border-spacing: 0;
  border-collapse: separate;
  width: 100%;
}

.datatable tr[scope='row']:hover {
  background-color: rgba(0, 0, 0, 0.03);
}

.datatable th {
  @apply relative bg-gray-150 px-2 font-bold align-middle select-none text-gray-600 text-sm;
  height: 3rem;
}

@screen lg {
  .datatable th {
    @apply sticky top-0;
  }
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
  @apply rounded-tl;
}
.datatable th:last-child {
  @apply rounded-tr;
}

@screen xl {
  .datatable th:first-child,
  .datatable td:first-child {
    @apply pl-6;
  }
  .datatable th:last-child,
  .datatable td:last-child {
    @apply pr-6;
  }
}

.datatable td {
  @apply px-2 align-middle border-b;
  height: 3.5rem;
  max-width: 25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.datatable td a {
  @apply flex items-center;
  min-width: 0;
  height: 3.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.datatable td a:hover {
  @apply underline;
}
</style>
