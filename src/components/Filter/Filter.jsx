import './Filter.css';

const FILTERS = [
  { label: 'All', value: 'all' },
  { label: 'Pending', value: 'pending' },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'Done', value: 'done' },
];

function Filter({ currentFilter, onFilterChange }) {
  return (
    <div className="filter-controls">
      {FILTERS.map(({ label, value }) => (
        <button
          key={value}
          className={currentFilter === value ? 'active' : ''}
          onClick={() => onFilterChange(value)}
        >
          {label}
        </button>
      ))}
    </div>
  );
}

export default Filter;