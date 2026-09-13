import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import { logout } from '../app/features/authSlice'
import toast from 'react-hot-toast'

const Navbar = () => {

    const dispatch = useDispatch()
    const { user } = useSelector(state => state.auth)
    const navigate = useNavigate()

    const logoutUser = () =>{
        dispatch(logout())
        navigate('/')
        toast.success('Account has been Logged Out!')
    }

    return (
        <div className='shadow bg-amber-100'>
            <nav className='flex items-center justify-between max-w-7xl mx-auto px-4 py-3.5 text-slate-800 transition-all'>
                <Link to='/'>
                    <img src="/logo.svg" alt="logo" className='h-11 w-auto' />
                </Link>
                <div className='flex items-center gap-4 text-sm'>
                    <p className='max-sm:hidden'>Hi, {user?.username.toUpperCase()}</p>
                    <button onClick={logoutUser} className='bg-white hover:bg-slate-100 border border-gray-300 px-7 py-1.5 rounded-full active:scale-95 transition-all'>Logout</button>
                </div>
            </nav>
        </div>
    )
}

export default Navbar