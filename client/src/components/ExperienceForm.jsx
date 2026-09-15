import { Briefcase, Loader2, Plus, Sparkles, Trash2Icon } from "lucide-react"
import api from "../config/api";
import { useSelector } from "react-redux";
import toast from "react-hot-toast";
import { useState } from "react";

const ExperienceForm = ({experiences, onChange, resumeId}) => {
    
    const { token } = useSelector(state => state.auth)
    const [ isGenerating, setIsGenerating ] = useState(false)

    const addExperience = async () =>{
        const newExperience = {
            company:'',
            position:'',
            start_date:null,
            end_date:null,
            description:'',
            is_current: false
        };
        try {
            const { data } = await api.post(`api/resume/${resumeId}/experiences/`, newExperience, {headers:{Authorization:`Bearer ${token}`}})
            console.log('is this working=', data.experience)
            onChange([...experiences, data.experience])
            toast.success('New Experience slot created.')
        } catch (error) {
            toast.error(
                error?.response?.data?.error ||
                error?.response?.data?.non_field_errors ||
                error?.message ||
                'Something went wrong'
            )
        }
    }
    const removeExperience = async (index, experienceId) =>{
        try {
            const { data } = await api.delete(`api/resume/${resumeId}/experiences/${experienceId}/delete/`, {headers:{Authorization:`Bearer ${token}`}})
            const updated = experiences.filter((_, i)=> i !== index);
            onChange(updated)
            toast.success(data.message)
        } catch (error) {
            toast.error(
                error?.response?.data?.error ||
                error?.response?.data?.non_field_errors ||
                error?.message ||
                'Something went wrong'
            )
        }
    }
    
    const updateExperience = (index, field, value)=>{
        const updated = [...experiences];
        updated[index] = {...updated[index], [field]:value}
        onChange(updated)
    }

    const enhanceDescription = async (index, description)=>{
        setIsGenerating(true)
        try {
            const { data } = await api.post(`api/resume/ai/enhance-job-desc/`, {userContent:description}, {headers:{Authorization:`Bearer ${token}`}})
            console.log(data)
            updateExperience(index, 'description', data.enhancedContent)
        } catch (error) {
            toast.error(
                error?.response?.data?.error ||
                error?.response?.data?.non_field_errors ||
                error?.message ||
                'Something went wrong'
            )
        } finally{
            setIsGenerating(false)
        }
    }
    return (
    <div className="space-y-6">
        <div className="flex items-center justify-between">
            <div>
                <h3 className="flex items-center gap-2 text-lg font-semibold text-gray-900">Professional Experience</h3>
                <p className="text-sm text-gray-500">Add your job experience</p>
            </div>
            <button onClick={addExperience} className="flex items-center gap-2 px-3 py-1 text-sm bg-green-100 text-geen-700 rounded-lg hover:bg-green-200">
                <Plus className="size-4" />
                Add Experience
            </button>
        </div>

        {experiences.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
                <Briefcase className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p>No work experience added yet.</p>
                <p className="text-sm">Click 'Add Experience' to get started.</p>
            </div>
        ): (
            <div className="space-y-4">
                {experiences.map((experience, index)=>(
                    <div key={index} className="p-4 border bordery-gray-200 rounded-lg space-y-3">
                        <div className="flex justify-between items-start">
                            <h4>Experience  #{index + 1}</h4>
                            <button onClick={()=> removeExperience(index, experience.id)} className='text-red-500 hover:text-red-700 transition-colors'>
                                <Trash2Icon className='size-4' />
                            </button>
                        </div>
                        <div className="grid md:grid-cols-2 gap-3">
                            <input value={experience.company || ''} onChange={(e)=>updateExperience(index, 'company', e.target.value)} type="text" placeholder="Company Name" className="px-3 py-2 text-sm rounded-lg" />
                            <input value={experience.position || ''} onChange={(e)=>updateExperience(index, 'position', e.target.value)} type="text" placeholder="Job Title" className="px-3 py-2 text-sm rounded-lg" />
                            <input value={experience.start_date || ''} onChange={(e)=>updateExperience(index, 'start_date', e.target.value)} type="month" className="px-3 py-2 text-sm rounded-lg" />
                            <input value={experience.end_date || ''} onChange={(e)=>updateExperience(index, 'end_date', e.target.value)} type="month" disabled={experience.is_current} className="px-3 py-2 text-sm rounded-lg disabled:bg-gray-100" />
                        </div>

                        <label htmlFor="" className="flex items-center gap-2">
                            <input type="checkbox" checked={experience.is_current || false} onChange={(e)=>{updateExperience(index, 'is_current', e.target.checked ? true : false); }} className="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                            <span className="text-sm text-gray-700">Currently working</span>
                        </label>

                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <label htmlFor="" className="text-sm font-medium text-gray-700">Job Description</label>
                                <button disabled={isGenerating} onClick={()=>enhanceDescription(index, experience.description)} className="flex items-center gap-1 px-2 py-1 text-xs bg-purple-100 text-purple-700 rounded hover:bg-purple-200 transition-colors disabled:opacity-50">
                                    {isGenerating ? (<Loader2 className="size-4 animate-spin" />): (<Sparkles className="w-3 h-3" />)}
                                    {isGenerating ? 'Enhancing...' : 'Enhance with AI'}
                                </button>
                            </div>
                            <textarea value={experience.description || ''} onChange={(e)=>{updateExperience(index, 'description', e.target.value)}} rows={4} className="w-full text-sm px-3 py-2 rounded-lg resize-none" placeholder="Describe your key responsibilities and achievements..."></textarea>
                        </div>
                    </div>
                ))}
            </div>
        )}
    </div>
  )
}

export default ExperienceForm