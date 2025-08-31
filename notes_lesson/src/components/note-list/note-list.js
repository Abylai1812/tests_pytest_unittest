import NoteListItem from '../note-list-item/note-list-item';

import './note-list.css';

const NoteList = ({data,onDelete,onToggleImportant}) => {
    const elements = data.map(item => {
    const {id,...itemProps} = item;
        return (
            <NoteListItem 
                key={id}
                {...itemProps}
                onDelete={() => onDelete(id)}
                onToggleImportant={() => onToggleImportant(id)}/>
        )
    })
    return (
        <div className="notes-list">
            {elements}
        </div>
    )
}

export default NoteList;