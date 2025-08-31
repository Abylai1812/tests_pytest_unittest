import './note-list-item.css';

const NoteListItem = (props) => {

        const {title,text,onDelete,onToggleImportant,important,date} = props;
         
        let classNames = "btn-star btn-sm";
        if ( important ) {
            classNames+= " important";
        }

        return (
            <div className='note'>
                <h5 className="title"> {title} </h5>
                <span>{text}</span>
                <div className="note-footer">
                    <small>{date}</small>
                    <button type="button"
                            className="btn-trash btn-sm"
                            onClick={onDelete}>
                            <i className="fas fa-trash"></i>
                        </button>
                    <button type="button"
                            className={classNames}
                            onClick={onToggleImportant}>
                        <i className="fas fa-star"></i>
                    </button>
                </div>
        </div>
        )

    }
    


export default NoteListItem;