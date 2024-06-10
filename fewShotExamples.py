#Fewshot examples
fewShot_examples = [
    
    #Assembledparts
    {
        "input": "How many parts were assembled last year?",
        "query": "SELECT COUNT(*) AS parts_assembled_last_year FROM assembledparts WHERE EXTRACT(YEAR FROM time) = EXTRACT(YEAR FROM CURRENT_DATE) - 1;",
    },
    
    {
        "input": "How many parts were assembled yesterday?",
        "query": "SELECT COUNT(*) AS parts_assembled_yesterday FROM assembledparts WHERE time = CURRENT_DATE - INTERVAL '1 day';",
    },
    
    {
        "input": "How many parts were assembled today?",
        "query": "SELECT COUNT(*) AS parts_assembled_today FROM assembledparts WHERE time = CURRENT_DATE;",
    },
    
    #projects
    {
        "input": "Which projects have been handled by architect 'HDR INC' ?",
        "query": "SELECT projectname FROM projects WHERE architect = 'HDR INC';",
    },
    
    {
        "input": "How many projects are active?",
        "query": "SELECT COUNT(*) AS active_projects FROM projects WHERE status = 'Active';",
    },
    
    #potemplatedata
    {
        "input": "What are the purchase order numbers and dates for 'Vendor A'?.",
        "query": "SELECT ponumber, date FROM potempaltedata WHERE vendor = 'Vendor A';",
    },
    
    #Workorders
    {
        "input": "How many workorders are unfinished?",
        "query": "SELECT COUNT(*) AS unfinished_workorders FROM workorders WHERE finished = 'false';",
    },
    
    {
        "input": "How many workorders are finished?",
        "query": "SELECT COUNT(*) FROM workorders WHERE finished = 'true';",
    },
    
    {
        "input": "How many workorders are done?",
        "query": "SELECT COUNT(*) FROM workorders WHERE finished = 'true';",
    },
    
    {
        "input": "Get all work orders assigned to User1?",
        "query": "SELECT * FROM workorders WHERE assignedto = 'User1';",
    },
    
    {
        "input": "List all work orders for the project 'BEACON'",
        "query": "SELECT * FROM workorders WHERE projectname = 'BEACON';",
    },
]
