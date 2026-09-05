import { BriefcaseBusiness, Globe, Link, Mail, MapPin, Phone, User } from "lucide-react"
import { useEffect, useState } from "react";


const PersonalInfoForm = ({data, onChange, removeBackground, setRemoveBackground}) => {
    
    const [previewUrl, setPreviewUrl] = useState(null);

    const handleChange = (field, value) =>{
        onChange({...data, [field]:value})
    }

    const fields = [
        { key: 'full_name', label: 'Full Name', icon: User, type:'text', required:true}, 
        { key: 'email', label: 'Email Id', icon: Mail, type:'text', required:true}, 
        { key: 'phone', label: 'Phone Number', icon: Phone, type:'tel'},
        { key: 'locatoin', label: 'Location', icon: MapPin, type:'text'},
        { key: 'profession', label: 'Profession', icon: BriefcaseBusiness, type:'text'},   
        { key: 'linkedin', label: 'LinkedIn Profile', icon: Link, type:'url'}, 
        { key: 'website', label: 'Personal Website', icon: Globe, type:'url'}, 
    ]
  
    useEffect(() => {
        if (!(data?.image instanceof File)) {
            setPreviewUrl(null);
            return;
        }

        const url = URL.createObjectURL(data.image);
        setPreviewUrl(url);

        return () => {
            URL.revokeObjectURL(url);
        };
    }, [data?.image]);
    return (
    <div>
        <h3 className="text-lg font-semibold text-gray-900">Personal Information</h3>
        <p className="text-sm text-gray-600">Get Started with the personal information</p>
        <div className="flex items-center gap-2">
            <label htmlFor="upload-profile-image">
                {data.image ? (
                    <img src={typeof data.image === 'string' ? data.image : previewUrl} alt="user-image" className="w-16 h-16 rounded-full object-cover mt-5 ring ring-slate-300 hover:opacity-80 cursor-pointer"/>
                ) : (
                    <div className="inline-flex items-center gap-2 mt-5 text-slate-600 hover:text-slate-700 cursor-pointer">
                        <User className="size-10 p-2.5 border rounded-full" />
                        upload user image
                    </div>
                )}
                <input id='upload-profile-image' type="file" accept="image/jpeg, image/png" className="hidden" onChange={(e)=>handleChange('image', e.target.files[0])} />
            </label>

            {data?.image instanceof File && (
                <div className="flex flex-col gap-1 pl-4 text-sm">
                    <p>Remove Background</p>
                    <label htmlFor="remove-background" className="relative inline-flex items-center cursor-pointer text-gray-900 gap-3">
                        <input id="remove-background" type="checkbox"className="sr-only peer" checked={removeBackground} onChange={(e) => setRemoveBackground(prev => !prev)}/>
                        <div className="w-9 h-5 bg-slate-300 rounded-full peer-checked:bg-green-600 transition-colors duration-200"></div>
                        <span className="absolute left-1 top-1 w-3 h-3 bg-white rounded-full transition-transform duration-200 ease-in-out peer-checked:translate-x-4"></span>
                    </label>
                </div>
                )}
        </div>

        {fields.map((field)=>{
            const Icon = field.icon
            return (
                <div key={field.key} className="spacey-y-1 mt-5">
                    <label htmlFor="" className="flex items-center gap-2 text-sm font-medium text-gray-600">
                        <Icon className='size-4' />
                        {field.label}
                        {field.required && <span className="text-red-500">*</span>}
                    </label>
                    <input type={field.type} value={data[field.key] || ''} onChange={(e)=>handleChange(field.key, e.target.value)} className="mt-1 w-full px-3 py-2 border border-gray-500 rounded-lg focus:ring focus:ring-blue-500 outline-none transition-colors text-sm" placeholder={`Enter your ${field.label.toLocaleLowerCase()}`} required={field.required} />
                </div>
            )
        })}
    </div>
  )
}

export default PersonalInfoForm