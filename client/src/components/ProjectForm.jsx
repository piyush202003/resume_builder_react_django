import { Plus, Projector, Trash2 } from "lucide-react"
import api from "../config/api"
import { useSelector } from "react-redux"
import toast from "react-hot-toast"

const ProjectForm = ({ data, onChange, resumeId }) => {
    
    const { token } = useSelector(state => state.auth)

    const addProject = async () =>{
        const newProject = {
            name:'',
            type:'',
            description:'',
        }
        try {
            const response = await api.post(`api/resume/${resumeId}/projects/`, newProject, {headers:{Authorization:`Bearer ${token}`}}) 
            onChange([...data, response.data.project])
            toast.success(response.data.message)
        } catch (error) {
            toast.error(
                error?.response?.data?.error ||
                error?.response?.data?.non_field_errors ||
                error?.message ||
                'Something went wrong'
            )
        }
    }

    async function removeProject (index, project_id){
        try {
            const response = await api.delete(`api/resume/${resumeId}/projects/${project_id}/delete/`, {headers:{Authorization:`Bearer ${token}`}})
            const updated = data.filter((_,i)=> i !== index)
            onChange(updated)
            console.log(response)
            toast.success(response.data.message)
        } catch (error) {
            toast.error(
                error?.response?.data?.error ||
                error?.response?.data?.non_field_errors ||
                error?.message ||
                'Something went wrong'
            )
        }
    }

    function updateProject(index, field, value) {
        const updated = [...data]
        updated[index] = {...updated[index], [field]:value}
        onChange(updated)
    }
    
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="flex items-center gap-2 text-lg font-semibold text-gray-900">Projects</h3>
                    <p className="text-sm text-gray-500">Add your Projects</p>
                </div>
                <button onClick={addProject} className="flex items-center gap-2 px-3 py-1 text-sm bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors">
                    <Plus className="size-4" /> Add Project
                </button>
            </div>

            {data.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                    <Projector className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                    <p>No project added yet.</p>
                    <p className="text-sm">Click 'Add Project' to get started.</p>
                </div>
            ):(
                <div className="space-y-4">
                    {data.map((project, index)=>(
                        <div key={index} className="p-4 border border-gray-200 rounded-lg space-y-3">
                            <div className="flex justify-between items-start">
                                <h4>Project #{index+1}</h4>
                                <button onClick={()=>removeProject(index, project.id)} className="text-red-500 hover:text-red-700 transition-colors">
                                    <Trash2 className="size-4" />
                                </button>
                            </div>

                            <div className="grid gap-3">
                                <input value={project.name || ''} onChange={(e)=>{updateProject(index, 'name', e.target.value)}} type="text" placeholder="Project Name" className="px-3 py-2 text-sm rounded-lg" />
                                <input value={project.type || ''} onChange={(e)=>{updateProject(index, 'type', e.target.value)}} type="text" placeholder="Project Type" className="px-3 py-2 text-sm rounded-lg" />
                                <textarea value={project.description || ''} onChange={(e)=>{updateProject(index, 'description', e.target.value)}} placeholder="Describe your project..." className="w-full px-3 py-2 text-sm rounded-lg resize-none" ></textarea>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

export default ProjectForm