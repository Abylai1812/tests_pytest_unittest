import "./app-filter.css";

const AppFilter = (props) => {

    const buttonsData = [ 
        {name:'all', label: 'All Notes'},
        {name:'important', label:'Important Notes'}  ];

    const buttons = buttonsData.map(({name,label}) => {
        const active = props.filter === name;
        const clazz = active ? 'btn-dark':'btn-outline-dark';
        
        return (
            <button type="button"
                   className={`btn ${clazz}`}
                   key={name}
                   onClick={() => props.onFilterSelect(name)}> 
                {label}  
            </button>
        )
    })

    return (
        <div className="btn-group">
           {buttons}
        </div>
    )
}

export default AppFilter;