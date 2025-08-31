

import './note-info.css';

const NoteInfo = ({notes,importanted}) => {
    return (
        <div>
            <h1 className="header">Notes App </h1>
            <h3 className="header-info">All notes: {notes}</h3>
            <h3 className="header-info">Important notes: {importanted}</h3>
        </div>
    )
}

export default NoteInfo;