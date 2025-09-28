import './TaskItem.css';

function TaskItem({ task, onDelete, onStatusChange }) {
  return (
    <div className={`task-item task-status-${task.status}`}>
      <div className="task-content">
        <h3>{task.title}</h3>
        <p>{task.description}</p>
      </div>
      <div className="task-controls">
        <select
          value={task.status}
          onChange={(e) => onStatusChange(task.id, e.target.value)}
        >
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
        <button className="delete-btn" onClick={() => onDelete(task.id)}>
          Delete
        </button>
      </div>
    </div>
  );
}

export default TaskItem;